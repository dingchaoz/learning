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

# # The agent pols data is depracated, need to use the new one once is available
# # will replace it later, use for now for just some areas analysis
# DFAgentPols = pd.read_csv('/san-data/usecase/agentpm/AgentProductionModel/agents_and_policies_auto.csv',header = None)
# # Add headers to the agent pol data
# agentPolHeaders =  ['POLICY_NUMBER','POLICY_KIND_CODE','PLCY_TYPE_CD','AGENT','AGENT_ASSIGN_TYPE_CD','AGENT_SERV_ST_CD_AGENT_CD','QMSLAT','QMSLON','STATUS_CODE','LOC_ADDR_01','LOC_CITY_NAME','LOC_ST_ABBR','LOC_ZIP','MARKET_UNIT_ID','DATE_EFFECTIVE_DATE','DATE_EXPIRATION_DATE','DATE_AGENT_ASSIGN_DATE','COUNTY','CITY','STATE','POSTL_ST_CD','STATE1','ZIP']
# DFAgentPols.columns = agentPolHeaders
# DFAgentPols.drop(DFAgentPols.columns[-2],axis = 1,inplace = True) #Drop the duplicated state1 column

# # Convert state column from int to string and display single digit with leading 0
# DFAgentPols['STATE'] = [str(x).zfill(2) for x in DFAgentPols['STATE']]

# # Load agent loc info as of 2016-09
# DFAgentLoc = pd.read_csv('/san-data/usecase/agentpm/AgentProductionModel/Agents_Sep_2016.csv')
# # Fill in the state agent code column for DFAgentPols, the corresponding column in agentsLoc is ST_AGT_CD
# DFAgentPols['AGENT_SERV_ST_CD_AGENT_CD'] = [x+str(y) for x,y in zip(DFAgentPols['STATE'],DFAgentPols['AGENT'])]


# # # Get agents located in Chicago, NY and SF which are urban metropolitans
# # sanfAgents = DFAgentLoc[DFAgentLoc.CITY == 'San Francisco']
# # newyorkAgents = DFAgentLoc[DFAgentLoc.CITY == 'New York']
# # chicagoAgents = DFAgentLoc[DFAgentLoc.CITY == 'Chicago']

# # # Merge chicago agents with their pols
# # chicagoAgentPols = chicagoAgents.merge(DFAgentPols,left_on = 'ST_AGT_CD',right_on = 'AGENT_SERV_ST_CD_AGENT_CD')
# # # Remove not needed or duplicated columns
# # chicagoAgentPols.drop(chicagoAgentPols[['ZIP','POSTL_ST_CD_y','STATE','CITY_y','COUNTY','AGENT_SERV_ST_CD_AGENT_CD','SF_RGN_CD','PREF_NM','ORGZN_NM']],axis = 1,inplace = True)

# # Make pol lat and long values valid
# def divide(x):
# 	try:
# 		return float(x)/1000000
# 	except:
# 		pass
# # chicagoAgentPols['QMSLAT'] = chicagoAgentPols['QMSLAT'].apply(divide)
# # chicagoAgentPols['QMSLON'] = chicagoAgentPols['QMSLON'].apply(divide)
# # chicagoAgentPols['lat_long_pol'] = chicagoAgentPols[['QMSLAT', 'QMSLON']].apply(tuple, axis=1)
# # chicagoAgentPols['lat_long_agent'] = chicagoAgentPols[['LATITUDE', 'LONGITUDE']].apply(tuple, axis=1)

# # Convert lat lon to utm
# def toUTM(x):
# 	try:
# 		return utm.from_latlon(x[0],x[1])[:2]
# 	except:
# 		pass
# # chicagoAgentPols['utm_pol'] = chicagoAgentPols['lat_long_pol'].apply(toUTM) 
# # chicagoAgentPols['utm_agent'] = chicagoAgentPols['lat_long_agent'].apply(toUTM)
# # scpy spatial distance:https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.pdist.html
# # A good discussion around disances computation http://stackoverflow.com/questions/13079563/how-does-condensed-distance-matrix-work-pdist

# #pdist(np.array([chicagoAgentPols['utm_pol'][0],chicagoAgentPols['utm_agent'][0]]))
# def getDist(x):
# 	try:
# 		#return pdist(np.array(x[0],x[1]))
# 		y = np.array([x[0],x[1]])
# 		#print pdist(y)
# 		return pdist(y)[0]
# 	except:
# 		pass

# ##Convert to datetimestamp from string 
# def getYear(x):
# 	return x[:4]
# # Get the first 5 digits zip code from the 9 digits zip format
# def getF5Zip(x):
# 	return x[:5]

# def getAssignDate(x):
# 	return x.DATE_AGENT_ASSIGN_DATE.dropna().value_counts().idxmax()

# def getTenure(x,y):
# 	try:
# 		deltaYr = relativedelta(pd.to_datetime(x), pd.to_datetime(y)).years
# 		return deltaYr
# 	except:
# 		pass

#     # Merge agent and their pols data
# DFMergedAgtPols = DFAgentLoc.merge(DFAgentPols,left_on = 'ST_AGT_CD',right_on = 'AGENT_SERV_ST_CD_AGENT_CD')
# DFMergedAgtPols.drop(DFMergedAgtPols[['ZIP','POSTL_ST_CD_y','STATE','CITY_y','COUNTY','AGENT_SERV_ST_CD_AGENT_CD','SF_RGN_CD','PREF_NM','ORGZN_NM']],axis = 1,inplace = True)
# 	# Prepare lat lon in the right format
# DFMergedAgtPols['QMSLAT'] = DFMergedAgtPols['QMSLAT'].apply(divide)
# DFMergedAgtPols['QMSLON'] = DFMergedAgtPols['QMSLON'].apply(divide)
# DFMergedAgtPols['lat_long_pol'] = DFMergedAgtPols[['QMSLAT', 'QMSLON']].apply(tuple, axis=1)
# DFMergedAgtPols['lat_long_agent'] = DFMergedAgtPols[['LATITUDE', 'LONGITUDE']].apply(tuple, axis=1)
# 	# Convert to utm from lat lon
# DFMergedAgtPols['utm_pol'] = DFMergedAgtPols['lat_long_pol'].apply(toUTM) 
# DFMergedAgtPols['utm_agent'] = DFMergedAgtPols['lat_long_agent'].apply(toUTM)
# DFMergedAgtPols['dist'] = DFMergedAgtPols[['utm_agent','utm_pol']].apply(getDist,axis = 1)
    
#     # Fill in nan for assignment date( NEED TO GET THE RIGHT AGENT APPOINTMENT DATE)
#     #DFMergedAgtPols['DATE_AGENT_ASSIGN_DATE'].fillna(method = 'backfill',inplace = True)
# DFMergedAgtPols['POL_YR'] = DFMergedAgtPols.DATE_EFFECTIVE_DATE.apply(getYear)
# DFMergedAgtPols['POL_ZIP'] = DFMergedAgtPols.LOC_ZIP.apply(getF5Zip)

### DFMergedAgtPols were saved into this file: /san-data/usecase/agentpm/AgentProductionModel/agtspols_processed.csv
os.chdir('/san-data/usecase/agentpm/AgentProductionModel/')
DFMergedAgtPols = pd.read_csv('agtspols_processed.csv')
# Get a list of all st agt code
allAgts = set(DFMergedAgtPols.ST_AGT_CD)

dfRes = pd.DataFrame()

for agt in allAgts:
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
	dfRes.append(res)
	print 'Res produced for agent', agt

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
