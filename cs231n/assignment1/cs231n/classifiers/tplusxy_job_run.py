import os
import pandas as pd
import numpy as np
import cPickle as pickle
import collections

os.chdir('/san-data/usecase/agentpm/AgentProductionModel/')

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
targets2015_aggfeatures2013 = pd.read_csv('datapull/targets2015_aggfeatures2013.csv')
#createXY(2014,2012)
targets2014_aggfeatures2012 = pd.read_csv('datapull/targets2014_aggfeatures2012.csv')
#createXY(2013,2011)
targets2013_aggfeatures2011 = pd.read_csv('datapull/targets2013_aggfeatures2011.csv')
tplus2XY = pd.concat([targets2015_aggfeatures2013,targets2014_aggfeatures2012,targets2013_aggfeatures2011],axis = 0)
tplus2XY.to_csv('datapull/tplus2XY.csv',index = None)
#########################################################
## tplus3 predict: 11->14,12->15
targets2015_aggfeatures2012 = pd.read_csv('datapull/targets2015_aggfeatures2012.csv')
#createXY(2014,2011)
targets2014_aggfeatures2011 = pd.read_csv('datapull/targets2014_aggfeatures2011.csv')
tplus3XY = pd.concat([targets2015_aggfeatures2012,targets2014_aggfeatures2011],axis = 0)
tplus3XY.to_csv('datapull/tplus3XY.csv',index = None)
#########################################################
## tplus4 predict: 11->15
targets2015_aggfeatures2011 = pd.read_csv('datapull/targets2015_aggfeatures2011.csv')
tplus4XY = targets2015_aggfeatures2011
tplus4XY.to_csv('datapull/tplus4XY.csv',index = None)
#########################################################
## tplus5 predict: 10->15
createXY(2015,2010)
targets2015_aggfeatures2010 = pd.read_csv('datapull/targets2015_aggfeatures2010.csv')
tplus5XY = targets2015_aggfeatures2010
# the agg features doesnot have agtstcode, thus append it from the tpluss4 which has the same
# pifsum and premsum
tplus5XY['agtstcode'] = yX_DF4.agtstcode
tplus5XY.to_csv('datapull/tplus5XY.csv',index = None)
