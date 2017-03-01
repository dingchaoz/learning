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

targets2015.to_csv('datapull/targets2015.csv')
##Use 2014 features predict for 2015
features2014 = pd.read_csv('top10ZipFeatures/top10ZipFeatures_2014.csv')