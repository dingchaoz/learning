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
targets = pd.read_csv('datapull/auto_agts_pif_prem_sum.csv',header = None)

##the intial file had two additional columns and no headers, and they got corrected:
# targets = targets.iloc[:,:7]
# header = ['year','agent_cd','st_cd','pol_effective_date','pol_expiration_date','pifsum','premsum']
# targets.columns = header
# targets.to_csv('datapull/auto_agts_pif_prem_sum.csv',index = None)

# Columns of effective and expirations dates can be compared directly
targets.pol_effective_date[0] >  targets.pol_expiration_date[0]
targets.pol_effective_date[0] >  '2011-01-01'

##Use 2014 features predict for 2015
features2014 = pd.read_csv('top10ZipFeatures/top10ZipFeatures_2014.csv')