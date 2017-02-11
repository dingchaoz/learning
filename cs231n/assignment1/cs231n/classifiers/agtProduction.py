import pandas as pd
import numpy as np
import os
# utm is installed by running python setup.py install in the directory at ejlq@da74wbedge1 [/home/ejlq/utm-0.4.1]
import utm
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist, squareform

os.chdir('/san-data/usecase/agentpm/AgentProductionModel')


# Add headers and new col
# Read sum aggregated auto prem columns grouped by state and agent code 
agtSumDF = pd.read_csv('auto_sum_stagt.csv',header = None)
# Add columns headers, the headers are in APM/Agent_Production_model.ipynb file
agtSumDF.columns = headers
# Create state agent column combining state and agent cols
agtSumDF.insert(1,'STCODE',[str(x)+str(y) for x,y in zip(agtSumDF['STATE'],agtSumDF['AGENT'])])
# Save to csv with added staget col and headers
agtSumDF.to_csv('auto_sum_stagt.csv',index = False)
# Drop NA any
agtSumDF.dropna(how = 'any',axis = 1, inplace = True)
# Save NA dropped file
agtSumDF.to_csv('auto_sum_stagt_nadropped.csv',index = False)


# ## The following is R code, converting from long to wide shape
# df <- read.csv('/san-data/usecase/agentpm/AgentProductionModel/auto_sum_stagt_nadropped.csv')
# dfAutoWide <- reshape(df, timevar = "YEAR",
#                       idvar = "STCODE",
#                       v.names = names(df)[3:83],
#                       direction = "wide")
# write.csv(dfAutoWide,file = '/san-data/usecase/agentpm/AgentProductionModel/auto_sum_stagt_nadropped_wide.csv',row.names=FALSE)

agtSumDFWide = pd.read_csv('auto_sum_stagt_nadropped_wide.csv')


# from statsmodels.stats.outliers_influence import variance_inflation_factor
# def calculate_vif_(X):
# thresh = 5.0
# variables = range(X.shape[1])
# dropped=True
# while (dropped==True):
#     dropped=False
#     vif = [variance_inflation_factor(X[variables].values, ix) for ix in range(X[variables].shape[1])]

#     maxloc = vif.index(max(vif))
#     if max(vif) > thresh:
#         print('dropping \'' + X[variables].columns[maxloc] + '\' at index: ' + str(maxloc))
#         del variables[maxloc]
#         dropped=True

# print('Remaining variables:')
# print(X.columns[variables])
# return X[variables]


# from statsmodels.stats.outliers_influence import variance_inflation_factor

def calculate_vif_(X):

    '''X - pandas dataframe'''
    thresh = 5.0
    variables = range(X.shape[1])

    for i in np.arange(0, len(variables)):
        vif = [variance_inflation_factor(X[variables].values, ix) for ix in range(X[variables].shape[1])]
        print(vif)
        maxloc = vif.index(max(vif))
        if max(vif) > thresh:
            print('dropping \'' + X[variables].columns[maxloc] + '\' at index: ' + str(maxloc))
            del variables[maxloc]

    print 'Remaining variables:'
    print X.columns[variables]
    return X