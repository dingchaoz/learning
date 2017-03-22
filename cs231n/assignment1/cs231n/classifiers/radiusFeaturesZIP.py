import pandas as pd
import numpy as np
import os
os.chdir('/san-data/usecase/agentpm/AgentProductionModel/radiusAnalysis/')

# the original top 10 source zips for each agent
dfRes = pd.read_csv('radiusZips.csv')

# Groupby homezip and tuple all top 10zips 
dfRes_byZip = dfRes.groupby('HOMEZIP')['TOP10ZIPS'].apply(lambda x: list(x)).reset_index()

list(dfRes_byZip[dfRes_byZip['HOMEZIP'] == '89117'].TOP10ZIPS)