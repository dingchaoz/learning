### result analysis
import os
import pandas as pd
import numpy as np

os.chdir('/san-data/usecase/agentpm/AgentProductionModel/')

# Get the last 6 years agent assignment info
DFAgentAssign = pd.read_excel('2010-2016New_Agent_Assignments.xlsx')

# Sum up multiple assginements
DFAgentAssign[['SUM_of_ASGN_A_POLS','SUM_of_ASGN_A_PREM','SUM_of_ASGN_F_PREM','SUM_of_ASGN_F_POLS']] \
= DFAgentAssign.groupby(['STCODE'])[['SUM_of_ASGN_A_POLS','SUM_of_ASGN_A_PREM','SUM_of_ASGN_F_PREM',\
'SUM_of_ASGN_F_POLS']] .transform('sum')

# Drop duplicates and only keep the first record
DFAgentAssign.drop_duplicates('STCODE',keep = 'first',inplace = True)

################################ To Analysis results################################
# This was saved from a RF model targeting 2015 pifsum, using tplu1XY.csv as features
res = pd.read_csv('datapull/res_analysis.csv')

# Chane col type the same before merge
res['agtstcode'] = [str(x) for x in res['agtstcode']]
DFAgentAssign['STCODE'] = [str(x) for x in DFAgentAssign['STCODE']]

# Merged for anlaysis
DFanalysis = res.merge(DFAgentAssign,left_on = 'agtstcode',right_on = 'STCODE')

DFanalysis = DFanalysis[['predict','prev_pifsum','pifsum','APPT_DATE']]

################################ To Create DataFrame XY for NEW agents################################


def newAgentXY(yX_DF):
	# Chane col type the same before merge
	yX_DF['agtstcode'] = [str(x) for x in yX_DF['agtstcode']]

	# Merged for new agents nonly
	yX_DF_NewAgents = yX_DF.merge(DFAgentAssign,left_on = 'agtstcode',right_on = 'STCODE')

	# Drop cols not needed
	del yX_DF_NewAgents['TERR_NAME']
	del yX_DF_NewAgents['NAME']
	del yX_DF_NewAgents['TERR']

	# Encode assignment type2 and determine if agents are new market agent 
	yX_DF_NewAgents['APPT_TYPE'] = yX_DF_NewAgents['APPT_TYPE'].replace('TICA',1)
	yX_DF_NewAgents['APPT_TYPE'] = yX_DF_NewAgents['APPT_TYPE'].replace('RPP',2)
	yX_DF_NewAgents['APPT_TYPE'] = yX_DF_NewAgents['APPT_TYPE'].replace('MOA',3)

	yX_DF_NewAgents['asgn_type2'] = yX_DF_NewAgents['asgn_type2'].replace('ALPHA',1)
	yX_DF_NewAgents['asgn_type2'] = yX_DF_NewAgents['asgn_type2'].replace('ZIP',2)

	# New market agents are identified TICA received with fewer than 500 auto and fire policies combined in the 1st year
	yX_DF_NewAgents['SUM'] = yX_DF_NewAgents.SUM_of_ASGN_F_POLS + yX_DF_NewAgents.SUM_of_ASGN_A_POLS
	yX_DF_NewAgents.loc[yX_DF_NewAgents.SUM < 500, 'NEW_MARKET'] = 1
	yX_DF_NewAgents.loc[yX_DF_NewAgents.SUM  >= 500, 'NEW_MARKET'] = 0
	del yX_DF_NewAgents['SUM']

	return yX_DF_NewAgents

## tplus1 new agents XY
yX_DF1 = pd.read_csv('datapull/tplus1XY.csv')
yX_DF_NewAgents1 = newAgentXY(yX_DF1)
yX_DF_NewAgents1.to_csv('datapull/tplus1XY_newAgents.csv',index = None)

## tplus2 new agents XY
yX_DF2 = pd.read_csv('datapull/tplus2XY.csv')
yX_DF_NewAgents2 = newAgentXY(yX_DF2)
yX_DF_NewAgents2.to_csv('datapull/tplus2XY_newAgents.csv',index = None)

## tplus4 new agents XY
yX_DF3 = pd.read_csv('datapull/tplus3XY.csv')
yX_DF_NewAgents3 = newAgentXY(yX_DF3)
yX_DF_NewAgents3.to_csv('datapull/tplus3XY_newAgents.csv',index = None)

## tplus4 new agents XY
yX_DF4 = pd.read_csv('datapull/tplus4XY.csv')
yX_DF_NewAgents4 = newAgentXY(yX_DF4)
yX_DF_NewAgents4.to_csv('datapull/tplus4XY_newAgents.csv',index = None)

## tplus5 new agents XY
yX_DF5 = pd.read_csv('datapull/tplus5XY.csv')
yX_DF_NewAgents5 = newAgentXY(yX_DF5)
yX_DF_NewAgents5.to_csv('datapull/tplus5XY_newAgents.csv',index = None)

##look at stuff in h2o
# hdfs dfs -ls output9/_temporary/1/_temporary/
