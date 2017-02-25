import pandas as pd
import numpy as np
# utm is installed by running python setup.py install in the directory at ejlq@da74wbedge1 [/home/ejlq/utm-0.4.1]
import utm
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist, squareform


# The agent pols data is depracated, need to use the new one once is available
# will replace it later, use for now for just some areas analysis
DFAgentPols = pd.read_csv('/san-data/usecase/agentpm/AgentProductionModel/datapull/agents_and_policies_auto.csv',header = None)
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


#newyorkAgentPols['TENURE'] = np.vectorize(getTenure)(newyorkAgentPols.DATE_EFFECTIVE_DATE,newyorkAgentPols.DATE_AGENT_ASSIGN_DATE)

#newyorkAgentPols.groupby(['ST_AGT_CD','TENURE']).POL_ZIP.nunique() #Return policy holder count zip for each agent
# newyorkAgentPols.groupby(['ST_AGT_CD','POL_YR']).POL_ZIP.nunique()
# newyorkAgentPols.groupby(['ST_AGT_CD','POL_YR','ZIP_CD']).POL_ZIP.nunique()
# newyorkAgentPols.groupby(['POL_YR']).POL_ZIP.nunique() # show trend overall year for certain areas
# Returns policy holder zips




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
    
    # Fill in nan for assignment date( NEED TO GET THE RIGHT AGENT APPOINTMENT DATE)
    #cityAgentPols['DATE_AGENT_ASSIGN_DATE'].fillna(method = 'backfill',inplace = True)
	cityAgentPols['POL_YR'] = cityAgentPols.DATE_EFFECTIVE_DATE.apply(getYear)
	cityAgentPols['POL_ZIP'] = cityAgentPols.LOC_ZIP.apply(getF5Zip)

	return cityAgentPols

def groupbyAnalysis(cityAgentPols):
	groupedSTAGT = cityAgentPols.groupby('ST_AGT_CD')
	DF_Dist_STAGT = groupedSTAGT['dist'].agg([np.mean,np.std])
	DF_Dist_STAGT['80Perc'] = groupedSTAGT['dist'].quantile(.8)
	DF_Dist_STAGT['90Perc'] = groupedSTAGT['dist'].quantile(.9)
	groupedZIP = cityAgentPols.groupby('ZIP_CD')
	DF_Dist_ZIP = groupedZIP['dist'].agg([np.mean,np.std])
	DF_Dist_ZIP['80Perc'] = groupedZIP['dist'].quantile(.8)
	DF_Dist_ZIP['90Perc'] = groupedZIP['dist'].quantile(.9)
	POL_ZIP_CNT = cityAgentPols.groupby(['ST_AGT_CD','POL_YR','ZIP_CD']).POL_ZIP.nunique()
	return DF_Dist_STAGT,DF_Dist_ZIP,POL_ZIP_CNT

newyorkAgentPols = cityAgentsPrep('New York')
NY_Dist_STAGT,NY_Dist_ZIP,NY_POL_ZIP = groupbyAnalysis(newyorkAgentPols)
chicagoAgentPols = cityAgentsPrep('Chicago')
CHG_Dist_STAGT,CHG_Dist_ZIP,CHG_POL_ZIP  = groupbyAnalysis(chicagoAgentPols)
sanfAgentPols = cityAgentsPrep('San Francisco')
SF_Dist_STAGT,SF_Dist_ZIP,SF_POL_ZIP  = groupbyAnalysis(sanfAgentPols)

#Reset index and add state column
NY_Dist_ZIP.reset_index(inplace = True)
NY_Dist_ZIP['ST'] = 'NY'
SF_Dist_ZIP.reset_index(inplace = True)
SF_Dist_ZIP['ST'] = 'SF'
CHG_Dist_ZIP.reset_index(inplace = True)
CHG_Dist_ZIP['ST'] = 'CHG'
DFZIPs = pd.concat([CHG_Dist_ZIP,SF_Dist_ZIP,NY_Dist_ZIP])


### TO-DO:
# Return neigbourhood zips number of agents, number of house hold, premium sum prediction, etc
# for all zips, agent tenure in the neigborhood (using existing zips, agents as training data)
# The returned will be the training Xs


########
# Seaborn plot analysis, 10040 agents in NY are outliers
########

## Look into agts10040
#agts10040 = newyorkAgentPols[newyorkAgentPols['ZIP_CD'] == '10040']


# chicagoAgentPols['dist'] = chicagoAgentPols[['utm_agent','utm_pol']].apply(getDist,axis = 1)
# grouped = chicagoAgentPols.groupby('ST_AGT_CD')
# grouped['dist'].agg([np.mean,np.std])
