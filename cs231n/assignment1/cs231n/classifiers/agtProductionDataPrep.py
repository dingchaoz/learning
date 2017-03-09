#import pyspark
#from pyspark import SparkContext, HiveContext, SparkConf
import os
import pandas as pd
import numpy as np
import cPickle as pickle
import collections

os.chdir('/san-data/usecase/agentpm/AgentProductionModel/')


## Re query the agents' pif and prem data without aggregating other columns
# may avoid the huge data file(>50 gs) and thus no need to spark
# sc = pyspark.SparkContext(appName="myAppName")
# sc._conf.getAll()

## Read the targets file
targets = pd.read_csv('datapull/auto_agts_pif_prem_sum.csv')

##the intial file had two additional columns and no headers, and they got corrected:
# targets = targets.iloc[:,:7]
# header = ['year','agent_cd','st_cd','pol_effective_date','pol_expiration_date','pifsum','premsum']
# targets.columns = header
# targets.to_csv('datapull/auto_agts_pif_prem_sum.csv',index = None)

# Columns of effective and expirations dates can be compared directly
targets.pol_effective_date[0] >  targets.pol_expiration_date[0]
targets.pol_effective_date[0] >  '2011-01-01'


# Get the active pol records at the end of each year

targets2011 = targets[targets.year == 2011]
targets2011 = targets2011[targets2011.pol_expiration_date >= '2012-01-01']

targets2012 = targets[targets.year == 2012]
targets2012 = targets2012[targets2012.pol_expiration_date >= '2013-01-01']

targets2013 = targets[targets.year == 2013]
targets2013 = targets2013[targets2013.pol_expiration_date >= '2014-01-01']

targets2014 = targets[targets.year == 2014]
targets2014 = targets2014[targets2014.pol_expiration_date >= '2015-01-01']

targets2015 = targets[targets.year == 2015]
targets2015 = targets2015[targets2015.pol_expiration_date >= '2016-01-01']

# Create agt state code column
targets2015['agtstcode'] = [str(x) +str(y) for x,y in zip(targets2015.st_cd,targets2015.agent_cd)]
targets2014['agtstcode'] = [str(x) +str(y) for x,y in zip(targets2014.st_cd,targets2014.agent_cd)]
targets2013['agtstcode'] = [str(x) +str(y) for x,y in zip(targets2013.st_cd,targets2013.agent_cd)]
targets2012['agtstcode'] = [str(x) +str(y) for x,y in zip(targets2012.st_cd,targets2012.agent_cd)]
targets2011['agtstcode'] = [str(x) +str(y) for x,y in zip(targets2011.st_cd,targets2011.agent_cd)]

del targets2011['agent_cd']
del targets2011['st_cd']
del targets2012['agent_cd']
del targets2012['st_cd']
del targets2013['agent_cd']
del targets2013['st_cd']
del targets2014['agent_cd']
del targets2014['st_cd']
del targets2015['agent_cd']
del targets2015['st_cd']


 # Group by agent code
 targets2015 = targets2015.groupby('agtstcode').agg(np.sum).reset_index()
 del targets2015['year']
 targets2014 = targets2014.groupby('agtstcode').agg(np.sum).reset_index()
 del targets2014['year']
 targets2013 = targets2013.groupby('agtstcode').agg(np.sum).reset_index()
 del targets2013['year']
 targets2012 = targets2012.groupby('agtstcode').agg(np.sum).reset_index()
 del targets2012['year']
 targets2011 = targets2011.groupby('agtstcode').agg(np.sum).reset_index()
 del targets2011['year']

 # Check if all home zips are digits(US), there are some of them are not
all([str(x).isdigit() for x in targets2015.agtstcode])

# Get the row index of canada agents
canadaIndex = [i for (i,x) in enumerate(targets2015.agtstcode) if not str(x).isdigit()]
# Remove canadian records
targets2015.drop(targets2015.index[canadaIndex],inplace = True)

# Get the row index of canada agents
canadaIndex = [i for (i,x) in enumerate(targets2014.agtstcode) if not str(x).isdigit()]
# Remove canadian records
targets2014.drop(targets2014.index[canadaIndex],inplace = True)

# Get the row index of canada agents
canadaIndex = [i for (i,x) in enumerate(targets2013.agtstcode) if not str(x).isdigit()]
# Remove canadian records
targets2013.drop(targets2013.index[canadaIndex],inplace = True)

# Get the row index of canada agents
canadaIndex = [i for (i,x) in enumerate(targets2012.agtstcode) if not str(x).isdigit()]
# Remove canadian records
targets2012.drop(targets2012.index[canadaIndex],inplace = True)

# Get the row index of canada agents
canadaIndex = [i for (i,x) in enumerate(targets2011.agtstcode) if not str(x).isdigit()]
# Remove canadian records
targets2011.drop(targets2011.index[canadaIndex],inplace = True)

targets2015.to_csv('datapull/targets2015.csv',index = None)
targets2014.to_csv('datapull/targets2014.csv',index = None)
targets2013.to_csv('datapull/targets2013.csv',index = None)
targets2012.to_csv('datapull/targets2012.csv',index = None)
targets2011.to_csv('datapull/targets2011.csv',index = None)


#########################################################
# Function to return xy data frame,give year of feature and year of target
def createXY(yTarget,yFeature):

	yFeature = str(yFeature)
	yTarget = str(yTarget)

	## Construct read file path
	targetsFilePath = 'datapull/targets' + yTarget +'.csv'
	featuresFilePath = 'top10ZipFeatures/top10ZipFeatures_' + yFeature +'.csv'

	## Contrucst export file path
	savetf_FilePath = 'datapull/targets' + yTarget +'_features' + yFeature +'.csv'
	saveaggf_FilePath = 'datapull/targets' + yTarget +'_aggfeatures' + yFeature +'.csv'
	# Read in features and targets
	features = pd.read_csv(featuresFilePath)
	targets = pd.read_csv(targetsFilePath)

	#Convert type from int to str before merge
	targets['agtstcode'] = [str(x) for x in targets['agtstcode']]

	# Join features with targets into one df, NOTE some agents in targets didn't have
	# any join of features: 19840 agent_st_cd in targets, 17506 agent code in features,11277 joined
	targets_features = targets.merge(features,left_on = 'agtstcode', right_on = 'ST_AGT_CD',how = 'inner')
	targets_features.to_csv(savetf_FilePath,index = None)

	# Create zip0-9 aggregated features
	uniquefeatures = targets_features.filter(regex = 'zip0').columns.tolist()
	uniquefeatures = [x.split('zip0_')[1] for x in uniquefeatures]


	# Create a placeholder for agged features
	agg_features = pd.DataFrame()
	for i,feature in enumerate(uniquefeatures):
		agg_features[i] = targets_features.filter(regex = feature).sum(axis = 1)

	# Add column name
	agg_features.columns = uniquefeatures
	# Add premsum and pifsum columns
	agg_features = pd.concat([targets_features.pifsum,targets_features.premsum,agg_features],axis = 1)
	agg_features.to_csv(saveaggf_FilePath,index = None)


#########################################################
##Use 2014 features predict for 2015
createXY(2015,2014)

#########################################################
##Use 2013 features predict for 2015
createXY(2015,2013)

#########################################################
##Use 2012 features predict for 2015
createXY(2015,2012)

#########################################################
##Use 2011 features predict for 2015
createXY(2015,2011)


######################################################### Agged Features Version
## tplus1 predict: 11->12,12->13,13->14,14->15
targets2015_aggfeatures2014 = pd.read_csv('datapull/targets2015_aggfeatures2014.csv')
createXY(2014,2013)
targets2014_aggfeatures2013 = pd.read_csv('datapull/targets2014_aggfeatures2013.csv')
createXY(2013,2012)
targets2013_aggfeatures2012 = pd.read_csv('datapull/targets2013_aggfeatures2012.csv')
createXY(2012,2011)
targets2012_aggfeatures2011 = pd.read_csv('datapull/targets2012_aggfeatures2011.csv')
tplus1XY = pd.concat([targets2015_aggfeatures2014,targets2014_aggfeatures2013,targets2013_aggfeatures2012,targets2012_aggfeatures2011],axis = 0)
tplus1XY.to_csv('datapull/tplus1XY.csv',index = None)
#########################################################
#########################################################
## tplus2 predict: 11->13, 12->14,13->15
targets2015_features2013 = pd.read_csv('datapull/targets2015_features2013.csv')
createXY(2014,2012)
targets2014_features2012 = pd.read_csv('datapull/targets2014_features2012.csv')
createXY(2013,2011)
targets2013_features2011 = pd.read_csv('datapull/targets2013_features2011.csv')
tplus2XY = pd.concat([targets2015_aggfeatures2013,targets2014_aggfeatures2012,targets2013_aggfeatures2011],axis = 0)
tplus2XY.to_csv('datapull/tplus2XY.csv',index = None)
#########################################################
## tplus3 predict: 11->14,12->15
targets2015_features2012 = pd.read_csv('datapull/targets2015_features2012.csv')
createXY(2014,2011)
targets2014_aggfeatures2011 = pd.read_csv('datapull/targets2014_features2011.csv')
tplus3XY = pd.concat([targets2015_aggfeatures2012,targets2014_aggfeatures2011],axis = 0)
tplus3XY.to_csv('datapull/tplus3XY.csv',index = None)
#########################################################
## tplus4 predict: 11->15
targets2015_features2011 = pd.read_csv('datapull/targets2015_features2011.csv')
tplus4XY = targets2015_aggfeatures2011
tplus4XY.to_csv('datapull/tplus4XY.csv',index = None)


######################################################### Add previous years
######################################################### pifsum and premsum as features
######################################################### as pure demo/bus pol features not
######################################################### predictive enough, this model
######################################################### is for ALL agents prod preeiction
######################################################### 
## tplus1 predict: 11->12,12->13,13->14,14->15
# Create prev premsum and prev pifum for non agged version tplus
targets2015_features2014 = pd.read_csv('datapull/targets2015_features2014.csv')
targets2014_features2013 = pd.read_csv('datapull/targets2014_features2013.csv')
targets2013_features2012 = pd.read_csv('datapull/targets2013_features2012.csv')
targets2012_features2011 = pd.read_csv('datapull/targets2012_features2011.csv')
targets2011 = pd.read_csv('datapull/targets2011.csv')
targets2015_features2014['prev_pifsum'] = targets2014_features2013['pifsum']
targets2015_features2014['prev_premsum'] = targets2014_features2013['premsum']
targets2014_features2013['prev_pifsum'] = targets2013_features2012['pifsum']
targets2014_features2013['prev_premsum'] = targets2013_features2012['premsum']
targets2013_features2012['prev_pifsum'] = targets2012_features2011['pifsum']
targets2013_features2012['prev_premsum'] = targets2012_features2011['premsum']
targets2012_features2011['prev_pifsum'] = targets2011['pifsum']
targets2012_features2011['prev_premsum'] = targets2011['premsum']
tplus1XY_nonagged = pd.concat([targets2015_features2014,targets2014_features2013,targets2013_features2012,targets2012_features2011],axis = 0)
tplus1XY_nonagged.to_csv('datapull/tplus1XY_nonagged.csv',index = None)

# Add agtcode, prev premsum and prev pifsum to agged version of tplus
tplus1XY = pd.read_csv('datapull/tplus1XY.csv')
tplus1XY_nonagged.reset_index(inplace = True)
tplus1XY['agtstcode'] = tplus1XY_nonagged['agtstcode']
tplus1XY['prev_pifsum'] = tplus1XY_nonagged['prev_pifsum']
tplus1XY['prev_premsum'] = tplus1XY_nonagged['prev_premsum']
tplus1XY.to_csv('datapull/tplus1XY.csv',index = None)
## tplus2 predict: 11->13, 12->14,13->15
targets2015_features2013 = pd.read_csv('datapull/targets2015_features2013.csv')
targets2014_features2012 = pd.read_csv('datapull/targets2014_features2012.csv')
targets2013_features2011 = pd.read_csv('datapull/targets2013_features2011.csv')

targets2012 = pd.read_csv('datapull/targets2012.csv')
targets2015_features2013['prev_pifsum'] = targets2013_features2011['pifsum']
targets2015_features2013['prev_premsum'] = targets2013_features2011['premsum']
targets2014_features2012['prev_pifsum'] = targets2012['pifsum']
targets2014_features2012['prev_premsum'] = targets2012['premsum']
targets2013_features2011['prev_pifsum'] = targets2011['pifsum']
targets2013_features2011['prev_premsum'] = targets2011['premsum']
tplus2XY_nonagged = pd.concat([targets2015_features2013,targets2014_features2012,targets2013_features2011],axis = 0)
tplus2XY_nonagged.to_csv('datapull/tplus2XY_nonagged.csv',index = None)

# Add agtcode, prev premsum and prev pifsum to agged version of tplus
tplus2XY = pd.read_csv('datapull/tplus2XY.csv')
tplus2XY_nonagged.reset_index(inplace = True)
tplus2XY['agtstcode'] = tplus2XY_nonagged['agtstcode']
tplus2XY['prev_pifsum'] = tplus2XY_nonagged['prev_pifsum']
tplus2XY['prev_premsum'] = tplus2XY_nonagged['prev_premsum']
tplus2XY.to_csv('datapull/tplus2XY.csv',index = None)

## tplus3 predict: 11->14, 12->15
targets2015_features2012 = pd.read_csv('datapull/targets2015_features2012.csv')
targets2014_features2011 = pd.read_csv('datapull/targets2014_features2011.csv')


targets2015_features2012['prev_pifsum'] = targets2012['pifsum']
targets2015_features2012['prev_premsum'] = targets2012['premsum']
targets2014_features2011['prev_pifsum'] = targets2011['pifsum']
targets2014_features2011['prev_premsum'] = targets2011['premsum']

tplus3XY_nonagged = pd.concat([targets2015_features2012,targets2014_features2011],axis = 0)
tplus3XY_nonagged.to_csv('datapull/tplus3XY_nonagged.csv',index = None)
# Add agtcode, prev premsum and prev pifsum to agged version of tplus
tplus3XY = pd.read_csv('datapull/tplus3XY.csv')
tplus3XY_nonagged.reset_index(inplace = True)
tplus3XY['agtstcode'] = tplus3XY_nonagged['agtstcode']
tplus3XY['prev_pifsum'] = tplus3XY_nonagged['prev_pifsum']
tplus3XY['prev_premsum'] = tplus3XY_nonagged['prev_premsum']
tplus3XY.to_csv('datapull/tplus3XY.csv',index = None)

## tplus4 predict: 11->15
targets2015_features2011 = pd.read_csv('datapull/targets2015_features2011.csv')
targets2015_features2011['prev_pifsum'] = targets2011['pifsum']
targets2015_features2011['prev_premsum'] = targets2011['premsum']
tplus4XY_nonagged = targets2015_features2011
tplus4XY_nonagged.to_csv('datapull/tplus4XY_nonagged.csv',index = None)

# Add agtcode, prev premsum and prev pifsum to agged version of tplus
tplus4XY = pd.read_csv('datapull/tplus4XY.csv')
tplus4XY_nonagged.reset_index(inplace = True)
tplus4XY['agtstcode'] = tplus4XY_nonagged['agtstcode']
tplus4XY['prev_pifsum'] = tplus4XY_nonagged['prev_pifsum']
tplus4XY['prev_premsum'] = tplus4XY_nonagged['prev_premsum']
tplus4XY.to_csv('datapull/tplus4XY.csv',index = None)
######################################################### Add agents tenure, assignment type
######################################################### features
######################################################### as pure demo/bus pol features not
######################################################### predictive enough, this model
######################################################### is for NEW agents prod preeiction
######################################################### 




