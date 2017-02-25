#import pyspark
from pyspark import SparkContext, HiveContext, SparkConf
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