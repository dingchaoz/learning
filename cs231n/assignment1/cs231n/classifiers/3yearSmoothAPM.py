import os
import pandas as pd
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error

###### For all agents model build: just try use last 3 years average
###### load all years' targets
targets2015 = pd.read_csv('datapull/targets2015.csv')
targets2014 = pd.read_csv('datapull/targets2014.csv')
targets2013 = pd.read_csv('datapull/targets2013.csv')
targets2012 = pd.read_csv('datapull/targets2012.csv')
targets2011 = pd.read_csv('datapull/targets2011.csv')

targets2011.columns = ['agtstcode','pifsum2011','premsum2011']
targets2012.columns = ['agtstcode','pifsum2012','premsum2012']
targets2013.columns = ['agtstcode','pifsum2013','premsum2013']
targets2014.columns = ['agtstcode','pifsum2014','premsum2014']
targets2015.columns = ['agtstcode','pifsum2015','premsum2015']


dfs = [targets2015,targets2014,targets2013,targets2012,targets2011]
df_final = reduce(lambda left,right:pd.merge(left,right, on = 'agtstcode'),dfs)

#take 3 year average from 2012 -2014
df_final['3yrAvg'] = df_final[['pifsum2014','pifsum2013','pifsum2012']].mean(axis = 1)
# the mae is 151, much smaller compared to 450 range in machine learning model
mean_absolute_error(df_final['3yrAvg'], df_final.pifsum2015)

# Now look at new agents only, see if 3 year would make sense
os.chdir('/san-data/usecase/agentpm/AgentProductionModel/')

# Get the last 6 years agent assignment info
DFAgentAssign = pd.read_excel('2010-2016New_Agent_Assignments.xlsx')

# Sum up multiple assginements
DFAgentAssign[['SUM_of_ASGN_A_POLS','SUM_of_ASGN_A_PREM','SUM_of_ASGN_F_PREM','SUM_of_ASGN_F_POLS']] \
= DFAgentAssign.groupby(['STCODE'])[['SUM_of_ASGN_A_POLS','SUM_of_ASGN_A_PREM','SUM_of_ASGN_F_PREM',\
'SUM_of_ASGN_F_POLS']] .transform('sum')

# Drop duplicates and only keep the first record
DFAgentAssign.drop_duplicates('STCODE',keep = 'first',inplace = True)
DFAgentAssign['STCODE'] = [str(x) for x in DFAgentAssign['STCODE']]
df_final['agtstcode'] = [str(x) for x in df_final['agtstcode']]

newAgentsTargets = df_final.merge(DFAgentAssign,left_on = 'agtstcode',right_on = 'STCODE')

newAgentsTargets['3yrAvg'] = newAgentsTargets[['pifsum2014','pifsum2013','pifsum2012']].mean(axis = 1)
