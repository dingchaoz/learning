import pandas as pd
import numpy as np
import os
# utm is installed by running python setup.py install in the directory at ejlq@da74wbedge1 [/home/ejlq/utm-0.4.1]
import utm
import collections
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist, squareform

### This script takes long to run, and it is better to run it in the backend
# http://askubuntu.com/questions/396654/how-to-run-the-python-program-in-the-background-in-ubuntu-machine
# :nohup python radius_production.py &
# see the program again use: ps ax | grep radius_production.py
# double check the nohup output using: tail nohup.out
# kill the program using top, u, then ejlq, then find the active python PID, kill it

### DFMergedAgtPols were saved into this file: /san-data/usecase/agentpm/AgentProductionModel/radiusAnalysis/agtspols_processed.csv
os.chdir('/san-data/usecase/agentpm/AgentProductionModel/radiusAnalysis/')
DFMergedAgtPols = pd.read_csv('agtspols_processed.csv')

# Get a list of all st agt code
allAgts = set(DFMergedAgtPols.ST_AGT_CD)

dfRes = pd.DataFrame()
i = 0

for agt in list(allAgts):
	# Get that agent's pol data into a df
	dfAgt = DFMergedAgtPols[DFMergedAgtPols['ST_AGT_CD'] == agt]
	print 'Extract data from agent ', agt
	# Sort the dfAgt by the pol distance to office
	dfAgt.sort('dist',inplace = True)
	print 'Dist sorted from agent', agt
	# Get the 80% number of pols for the agent
	numPols = int(round(dfAgt.shape[0]*0.8))
	# Counter count the zips that has 80% of the pols
	c = collections.Counter(dfAgt.POL_ZIP[:numPols])
	# Get the top 10 zips that has the most number of pols
	top10Zips = c.most_common(10)
	print 'Top 10 zips produced for agent', agt
	# Initiate array to hold the result data which has st_agt_cd,home_zip and top 10 zips that have most pols
	res = [agt,dfAgt.ZIP_CD.iloc[0]]
	res.append([x[0] for x in top10Zips])
	res = [res]
	dfRes = dfRes.append(res)
	print 'Res produced for agent', agt
	i += 1
	if i % 100 == 0:
		dfRes.to_pickle('radiusZips')
	print 'pick dumped ', i

dfRes.to_pickle('radiusZips')
#dfRes = pd.read_pickle(file_name)
dfRes.to_csv('radiusZips.csv')



#One example: 
# agt011032 = DFMergedAgtPols[DFMergedAgtPols['ST_AGT_CD'] == 11032]
# agt011032.sort('dist',inplace = True)
# set(agt011032.POL_ZIP)
# i = agt011032.shape[0]
# import collections
# c = collections.Counter(agt011032.POL_ZIP[:int(i)])
# x = c.most_common(10)
# a = [[x1[0] for x1 in x]]
