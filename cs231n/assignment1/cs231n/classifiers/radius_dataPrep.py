import pandas as pd
import numpy as np
import os
# utm is installed by running python setup.py install in the directory at ejlq@da74wbedge1 [/home/ejlq/utm-0.4.1]
import utm
import collections
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist, squareform


# The agent pols data is depracated, need to use the new one once is available
# will replace it later, use for now for just some areas analysis
os.chdir('/san-data/usecase/agentpm/AgentProductionModel/')
DFAgentPols = pd.read_csv('datapull/agents_and_policies_auto.csv',header = None)
# Add headers to the agent pol data
agentPolHeaders =  ['POLICY_NUMBER','POLICY_KIND_CODE','PLCY_TYPE_CD','AGENT','AGENT_ASSIGN_TYPE_CD','AGENT_SERV_ST_CD_AGENT_CD','QMSLAT','QMSLON','STATUS_CODE','LOC_ADDR_01','LOC_CITY_NAME','LOC_ST_ABBR','LOC_ZIP','MARKET_UNIT_ID','DATE_EFFECTIVE_DATE','DATE_EXPIRATION_DATE','DATE_AGENT_ASSIGN_DATE','COUNTY','CITY','STATE','POSTL_ST_CD','STATE1','ZIP']
DFAgentPols.columns = agentPolHeaders
DFAgentPols.drop(DFAgentPols.columns[-2],axis = 1,inplace = True) #Drop the duplicated state1 column

# Convert state column from int to string and display single digit with leading 0
DFAgentPols['STATE'] = [str(x).zfill(2) for x in DFAgentPols['STATE']]

# Load agent loc info as of 2016-09
DFAgentLoc = pd.read_csv('Agents_Sep_2016.csv')
# Fill in the state agent code column for DFAgentPols, the corresponding column in agentsLoc is ST_AGT_CD
DFAgentPols['AGENT_SERV_ST_CD_AGENT_CD'] = [x+str(y) for x,y in zip(DFAgentPols['STATE'],DFAgentPols['AGENT'])]




# Make pol lat and long values valid
def divide(x):
	try:
		return float(x)/1000000
	except:
		pass

# Convert lat lon to utm
def toUTM(x):
	try:
		return utm.from_latlon(x[0],x[1])[:2]
	except:
		pass


def getDist(x):
	try:
		#return pdist(np.array(x[0],x[1]))
		y = np.array([x[0],x[1]])
		#print pdist(y)
		return pdist(y)[0]
	except:
		pass

##Convert to datetimestamp from string 
def getYear(x):
	return x[:4]
# Get the first 5 digits zip code from the 9 digits zip format
def getF5Zip(x):
	return x[:5]

def getAssignDate(x):
	return x.DATE_AGENT_ASSIGN_DATE.dropna().value_counts().idxmax()

def getTenure(x,y):
	try:
		deltaYr = relativedelta(pd.to_datetime(x), pd.to_datetime(y)).years
		return deltaYr
	except:
		pass

    # Merge agent and their pols data
DFMergedAgtPols = DFAgentLoc.merge(DFAgentPols,left_on = 'ST_AGT_CD',right_on = 'AGENT_SERV_ST_CD_AGENT_CD')
DFMergedAgtPols.drop(DFMergedAgtPols[['ZIP','POSTL_ST_CD_y','STATE','CITY_y','COUNTY','AGENT_SERV_ST_CD_AGENT_CD','SF_RGN_CD','PREF_NM','ORGZN_NM']],axis = 1,inplace = True)
	# Prepare lat lon in the right format
DFMergedAgtPols['QMSLAT'] = DFMergedAgtPols['QMSLAT'].apply(divide)
DFMergedAgtPols['QMSLON'] = DFMergedAgtPols['QMSLON'].apply(divide)
DFMergedAgtPols['lat_long_pol'] = DFMergedAgtPols[['QMSLAT', 'QMSLON']].apply(tuple, axis=1)
DFMergedAgtPols['lat_long_agent'] = DFMergedAgtPols[['LATITUDE', 'LONGITUDE']].apply(tuple, axis=1)
	# Convert to utm from lat lon
DFMergedAgtPols['utm_pol'] = DFMergedAgtPols['lat_long_pol'].apply(toUTM) 
DFMergedAgtPols['utm_agent'] = DFMergedAgtPols['lat_long_agent'].apply(toUTM)
DFMergedAgtPols['dist'] = DFMergedAgtPols[['utm_agent','utm_pol']].apply(getDist,axis = 1)
    
# Get the pol year and first 5 digit of pol zip
DFMergedAgtPols['POL_YR'] = DFMergedAgtPols.DATE_EFFECTIVE_DATE.apply(getYear)
DFMergedAgtPols['POL_ZIP'] = DFMergedAgtPols.LOC_ZIP.apply(getF5Zip)


DFMergedAgtPols.to_csv('radiusAnalysis/agtspols_processed.csv')