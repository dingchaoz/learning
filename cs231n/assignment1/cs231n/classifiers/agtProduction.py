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