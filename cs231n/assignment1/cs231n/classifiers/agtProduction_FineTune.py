# https://github.com/h2oai/h2o-tutorials/blob/master/tutorials/gbm-randomforest/GBM_RandomForest_Example.py
import os
import pandas as pd
import numpy as np
import cPickle as pickle
import collections
import matplotlib.pyplot as plt
from sklearn import ensemble
from sklearn import datasets
from sklearn import svm
import h2o
import math
from h2o.estimators.gbm import H2OGradientBoostingEstimator
from h2o.grid.grid_search import H2OGridSearch
from h2o.estimators.random_forest import H2ORandomForestEstimator
h2o.connect(ip = '10.96.242.158', port = '54321')

os.chdir('/san-data/usecase/agentpm/AgentProductionModel/')

# agg_features2015 = pd.read_csv('datapull/targets_aggfeatures2015.csv')
# targets_features2015 = pd.read_csv('datapull/targets_features2015.csv')

##########################################
#note: 2017-03-08 so far tried agged and non agged version of single 14-15 train predict
# mape is about 30%, mae 470, average pifsum is 1400, so not good result

###### the single year train predict data loading :
# Put the xy together in one data frame in aggregated feature form
#yX_DF = pd.concat([targets_features2015.pifsum,targets_features2015.premsum,agg_features2015],axis = 1)
#None aggregated feature dataset
#yX_DF = targets_features2015.drop(['agtstcode','ST_AGT_CD'],axis = 1)

# Get the last 6 years agent assignment info
DFAgentLoc = pd.read_csv('Agents_Sep_2016.csv')

###### use the 11,12,13,14 --> 15, mae goes down to 412, better but still too high for pifsum
###### did the same thing for premsum predict, mape is also 29%
yX_DF = pd.read_csv('datapull/tplus1XY.csv')


###H2O run:
dfTrain = yX_DF.drop(['pifsum','premsum','agtstcode'],axis = 1)

# Convert the dfs into H2O format
# dfAuto_h2o has all the columns
# dfAuto_train has only the train columns
dfAuto_h2o = h2o.H2OFrame(python_obj = yX_DF.to_dict('list'))
dfAuto_train = h2o.H2OFrame(python_obj=dfTrain.to_dict('list'))

## the response variable
response = 'pifsum'
dfAuto_h2o[response] = dfAuto_h2o[response]         

## use all other columns (except for the name & the response column ("survived")) as predictors
predictors = dfAuto_train.columns

# Split the data for Machine Learning
train, valid, test = dfAuto_h2o.split_frame(
    ratios=[0.6,0.2], 
    seed=1234, 
    destination_frames=['train.hex','valid.hex','test.hex']
)

rf_v1 = H2ORandomForestEstimator(
    model_id="rf_covType_v1",
    ntrees=200,
    stopping_rounds=2,
    score_each_iteration=True,
    seed=1000000)

rf_v1.train(x=predictors, y=response, training_frame=train, validation_frame=valid)

#evaluate result on valid dataset
rf_v1.model_performance(valid)

truth = h2o.as_list(valid).pifsum
prev_truth = h2o.as_list(valid).prev_pifsum
predict = h2o.as_list(rf_v1.predict(valid))
agtstcode = h2o.as_list(valid).agtstcode
pd.concat([agtstcode,predict,prev_truth,truth],axis = 1)

## save_Model, doesn't work got access issue: h2o.save_model(rfv1,'home/ejlq',force = True)
# so i had to use the GUI to export it, seems the model is saved on the worker node of h2o
# that is running the job
# the loading back/ import works md = h2o.load_model('home/ejlq')


# We used a default random forest. Random forest's primary strength is how well it runs with standard parameters, and while there are only a few parameters to tune, we can experiment with those to see if it will make a difference.  
# 
# The main parameters to tune are the tree depth and the mtries, which is the number of predictors to use.  
# 
# The default depth of trees is 20. It is common to increase this number, to the point that in some implementations, the depth is unlimited. We will increase ours from 20 to 30.  
# 
# Note that the default mtries depends on whether classification or regression is being run. The default for classification is one-third of the columns. The default for regression is the square root of the number of columns.  

# ### Random Forest #2

# In[ ]:

rf_v2 = H2ORandomForestEstimator(
    model_id="rf_covType_v2",
    ntrees=200,
    max_depth=30,
    stopping_rounds=2,
    stopping_tolerance=0.01,
    score_each_iteration=True,
    seed=3000000)
rf_v2.train(x=predictors, y=response, training_frame=train, validation_frame=valid)
rf_v2.model_performance(valid)

#v3 gbm
gbm_v3 = H2OGradientBoostingEstimator(
    ntrees=300,
    learn_rate=0.3,
    max_depth=10,
    sample_rate=0.7,
    col_sample_rate=0.7,
    stopping_rounds=2,
    stopping_tolerance=0.01, #10-fold increase in threshold as defined in rf_v1
    score_each_iteration=True,
    model_id="gbm_covType_v3",
    seed=2000000
)
gbm_v3.train(x=predictors, y=response, training_frame=train, validation_frame=valid)
gbm_v3.model_performance(valid)