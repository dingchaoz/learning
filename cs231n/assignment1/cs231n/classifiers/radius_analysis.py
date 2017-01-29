import pandas as pd
import numpy as np
# utm is installed by running python setup.py install in the directory at ejlq@da74wbedge1 [/home/ejlq/utm-0.4.1]
import utm
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist, squareform


# The agent pols data is depracated, need to use the new one once is available
# will replace it later, use for now for just some areas analysis
DFAgentPols = pd.read_csv('/san-data/usecase/agentpm/AgentProductionModel/agents_and_policies_auto.csv',header = None)
# Add headers to the agent pol data
agentPolHeaders =  ['POLICY_NUMBER','POLICY_KIND_CODE','PLCY_TYPE_CD','AGENT','AGENT_ASSIGN_TYPE_CD','AGENT_SERV_ST_CD_AGENT_CD','QMSLAT','QMSLON','STATUS_CODE','LOC_ADDR_01','LOC_CITY_NAME','LOC_ST_ABBR','LOC_ZIP','MARKET_UNIT_ID','DATE_EFFECTIVE_DATE','DATE_EXPIRATION_DATE','DATE_AGENT_ASSIGN_DATE','COUNTY','CITY','STATE','POSTL_ST_CD','STATE1','ZIP']
DFAgentPols.columns = agentPolHeaders
DFAgentPols.drop(DFAgentPols.columns[-2],axis = 1,inplace = True) #Drop the duplicated state1 column

# Convert state column from int to string and display single digit with leading 0
DFAgentPols['STATE'] = [str(x).zfill(2) for x in DFAgentPols['STATE']]

# Load agent loc info as of 2016-09
DFAgentLoc = pd.read_csv('/san-data/usecase/agentpm/AgentProductionModel/Agents_Sep_2016.csv')
# Fill in the state agent code column for DFAgentPols, the corresponding column in agentsLoc is ST_AGT_CD
DFAgentPols['AGENT_SERV_ST_CD_AGENT_CD'] = [x+str(y) for x,y in zip(DFAgentPols['STATE'],DFAgentPols['AGENT'])]


# # Get agents located in Chicago, NY and SF which are urban metropolitans
# sanfAgents = DFAgentLoc[DFAgentLoc.CITY == 'San Francisco']
# newyorkAgents = DFAgentLoc[DFAgentLoc.CITY == 'New York']
# chicagoAgents = DFAgentLoc[DFAgentLoc.CITY == 'Chicago']

# # Merge chicago agents with their pols
# chicagoAgentPols = chicagoAgents.merge(DFAgentPols,left_on = 'ST_AGT_CD',right_on = 'AGENT_SERV_ST_CD_AGENT_CD')
# # Remove not needed or duplicated columns
# chicagoAgentPols.drop(chicagoAgentPols[['ZIP','POSTL_ST_CD_y','STATE','CITY_y','COUNTY','AGENT_SERV_ST_CD_AGENT_CD','SF_RGN_CD','PREF_NM','ORGZN_NM']],axis = 1,inplace = True)

# Make pol lat and long values valid
def divide(x):
	try:
		return float(x)/1000000
	except:
		pass
# chicagoAgentPols['QMSLAT'] = chicagoAgentPols['QMSLAT'].apply(divide)
# chicagoAgentPols['QMSLON'] = chicagoAgentPols['QMSLON'].apply(divide)
# chicagoAgentPols['lat_long_pol'] = chicagoAgentPols[['QMSLAT', 'QMSLON']].apply(tuple, axis=1)
# chicagoAgentPols['lat_long_agent'] = chicagoAgentPols[['LATITUDE', 'LONGITUDE']].apply(tuple, axis=1)

# Convert lat lon to utm
def toUTM(x):
	try:
		return utm.from_latlon(x[0],x[1])[:2]
	except:
		pass
# chicagoAgentPols['utm_pol'] = chicagoAgentPols['lat_long_pol'].apply(toUTM) 
# chicagoAgentPols['utm_agent'] = chicagoAgentPols['lat_long_agent'].apply(toUTM)
# scpy spatial distance:https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.pdist.html
# A good discussion around disances computation http://stackoverflow.com/questions/13079563/how-does-condensed-distance-matrix-work-pdist

#pdist(np.array([chicagoAgentPols['utm_pol'][0],chicagoAgentPols['utm_agent'][0]]))
def getDist(x):
	try:
		#return pdist(np.array(x[0],x[1]))
		y = np.array([x[0],x[1]])
		#print pdist(y)
		return pdist(y)[0]
	except:
		pass

def cityAgentsPrep(cityName):
	cityAgents = DFAgentLoc[DFAgentLoc.CITY == cityName]
	#Merge chicago agents with their pols
	cityAgentPols = cityAgents.merge(DFAgentPols,left_on = 'ST_AGT_CD',right_on = 'AGENT_SERV_ST_CD_AGENT_CD')
	# Remove not needed or duplicated columns
	cityAgentPols.drop(cityAgentPols[['ZIP','POSTL_ST_CD_y','STATE','CITY_y','COUNTY','AGENT_SERV_ST_CD_AGENT_CD','SF_RGN_CD','PREF_NM','ORGZN_NM']],axis = 1,inplace = True)
	# Prepare lat lon in the right format
	cityAgentPols['QMSLAT'] = cityAgentPols['QMSLAT'].apply(divide)
	cityAgentPols['QMSLON'] = cityAgentPols['QMSLON'].apply(divide)
	cityAgentPols['lat_long_pol'] = cityAgentPols[['QMSLAT', 'QMSLON']].apply(tuple, axis=1)
	cityAgentPols['lat_long_agent'] = cityAgentPols[['LATITUDE', 'LONGITUDE']].apply(tuple, axis=1)
	# Convert to utm from lat lon
	cityAgentPols['utm_pol'] = cityAgentPols['lat_long_pol'].apply(toUTM) 
	cityAgentPols['utm_agent'] = cityAgentPols['lat_long_agent'].apply(toUTM)
	cityAgentPols['dist'] = cityAgentPols[['utm_agent','utm_pol']].apply(getDist,axis = 1)

	return cityAgentPols

def groupbyAnalysis(cityAgentPols):
	groupedSTAGT = cityAgentPols.groupby('ST_AGT_CD')
	DF_Dist_STAGT = groupedSTAGT['dist'].agg([np.mean,np.std])
	groupedZIP = cityAgentPols.groupby('ZIP_CD')
	DF_Dist_ZIP = groupedZIP['dist'].agg([np.mean,np.std])
	return DF_Dist_STAGT,DF_Dist_ZIP

newyorkAgentPols = cityAgentsPrep('New York')
NY_Dist_STAGT,NY_Dist_ZIP = groupbyAnalysis(newyorkAgentPols)
chicagoAgentPols = cityAgentsPrep('Chicago')
CHG_Dist_STAGT,CHG_Dist_ZIP = groupbyAnalysis(chicagoAgentPols)
sanfAgentPols = cityAgentsPrep('San Francisco')
SF_Dist_STAGT,SF_Dist_ZIP = groupbyAnalysis(sanfAgentPols)



# chicagoAgentPols['dist'] = chicagoAgentPols[['utm_agent','utm_pol']].apply(getDist,axis = 1)
# grouped = chicagoAgentPols.groupby('ST_AGT_CD')
# grouped['dist'].agg([np.mean,np.std])
