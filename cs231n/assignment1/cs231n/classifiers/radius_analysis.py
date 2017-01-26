import pandas as pd


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


# Get agents located in Chicago, NY and SF which are urban metropolitans
sanfAgents = DFAgentLoc[DFAgentLoc.CITY == 'San Francisco']
newyorkAgents = DFAgentLoc[DFAgentLoc.CITY == 'New York']
chicagoAgents = DFAgentLoc[DFAgentLoc.CITY == 'Chicago']

# Merge chicago agents with their pols
chicagoAgentPols = chicagoAgents.merge(DFAgentPols,left_on = 'ST_AGT_CD',right_on = 'AGENT_SERV_ST_CD_AGENT_CD')
# Remove not needed or duplicated columns
chicagoAgentPols.drop(chicagoAgentPols[['ZIP','POSTL_ST_CD_y','STATE','CITY_y','COUNTY','AGENT_SERV_ST_CD_AGENT_CD','SF_RGN_CD', 'ZIP_CD','PREF_NM','ORGZN_NM']],axis = 1,inplace = True)
# Make pol lat and long values valid
def divide(x):
	try:
		return float(x)/1000000
	except:
		pass
chicagoAgentPols['QMSLAT'] = chicagoAgentPols['QMSLAT'].apply(divide)
chicagoAgentPols['QMSLON'] = chicagoAgentPols['QMSLON'].apply(divide)