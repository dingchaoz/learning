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
h2o.connect(ip = '10.96.242.230', port = '54321')


os.chdir('/san-data/usecase/agentpm/AgentProductionModel/')

agg_features2015 = pd.read_csv('datapull/targets_aggfeatures2015.csv')
targets_features2015 = pd.read_csv('datapull/targets_features2015.csv')

# Put the xy together in one data frame
yX_DF = pd.concat([targets_features2015.pifsum,targets_features2015.premsum,agg_features2015],axis = 1)

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
dfTrain = yX_DF.drop(['pifsum','premsum'],axis = 1)

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

## Get the metrics on the validation set
perf = gbm.model_performance(valid)
print perf

from sklearn.utils import check_array
def mape(y_true, y_pred): 
 
        return np.mean([np.abs(x - y) for x, y in zip(y_true, y_pred)])/ np.mean(y_true)

truth = h2o.as_list(valid).pifsum
predict = h2o.as_list(gbm.predict(valid))
pd.concat([predict,truth],axis = 1)

##the mae is 464, and the pifsum avg is about 1481, error too high

