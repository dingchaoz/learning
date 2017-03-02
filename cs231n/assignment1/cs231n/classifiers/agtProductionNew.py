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

##Use 2014 features predict for 2015
features2014 = pd.read_csv('top10ZipFeatures/top10ZipFeatures_2014.csv')
# Join features with targets into one df, NOTE some agents in targets didn't have
# any join of features: 19840 agent_st_cd in targets, 17506 agent code in features,11277 joined
targets_featues2015 = targets2015.merge(features2014,left_on = 'agtstcode', right_on = 'ST_AGT_CD',how = 'inner')
