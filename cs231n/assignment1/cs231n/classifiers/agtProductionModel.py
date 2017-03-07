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
import pandas as pd
h2o.connect(ip = '10.96.242.158', port = '54321')

os.chdir('/san-data/usecase/agentpm/AgentProductionModel/')

agg_features2015 = pd.read_csv('datapull/targets_aggfeatures2015.csv')
targets_features2015 = pd.read_csv('datapull/targets_features2015.csv')

# y = targets_features2015.pifsum
# #X = targets_features2015.iloc[:,18:]
# X = agg_features2015
# X.fillna(value = 0,inplace = True)
# y.fillna(value = 0,inplace = True)

# X = X.astype(np.float32)

# offset = int(X.shape[0] * 0.7)
# X_train, y_train = X[:offset], y[:offset]
# X_test, y_test = X[offset:], y[offset:]

###H2O run:
dfTrain = agg_features2015

# Convert the dfs into H2O format
# dfAuto_h2o has all the columns
# dfAuto_train has only the train columns
dfAuto_h2o = h2o.H2OFrame(python_obj = targets_features2015.to_dict('list'))
dfAuto_train = h2o.H2OFrame(python_obj=dfTrain.to_dict('list'))

## the response variable
response = 'pifsum'
dfAuto_h2o[response] = dfAuto_h2o[response]         

## use all other columns (except for the name & the response column ("survived")) as predictors
predictors = dfAuto_train.columns

# Split the data for Machine Learning
train, valid = dfAuto_h2o.split_frame(
    ratios=[0.7], 
    seed=1234, 
    destination_frames=['train.hex','valid.hex']
)

import numpy as np
import math
from h2o.estimators.gbm import H2OGradientBoostingEstimator
from h2o.grid.grid_search import H2OGridSearch

#We only provide the required parameters, everything else is default
gbm = H2OGradientBoostingEstimator()
gbm.train(x=predictors, y=response, training_frame=train)

## Show a detailed model summary
print gbm


