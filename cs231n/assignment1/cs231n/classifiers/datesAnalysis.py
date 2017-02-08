import pandas as pd
import numpy as np
import os
os.chdir('/san-data/usecase/agentpm/AgentProductionModel')
d47201 = pd.read_csv('allautocolumns47201.csv',header = None)
cols = pd.read_csv('prem_columns.csv')
headers = [x.split('auto_prem_ytd_snapshot')[1] for x in list(cols.columns)]
d47201.columns = headers
# datesonly = d47201.filter(regex=('.date*'))
# datesonly = pd.concat((datesonly,d47201['.policy_number']),axis = 1)

# Get pol data
polsDF = pd.concat((d47201['.agent'],d47201['.year_month'],d47201['.policy_number'],d47201['.date_agent_assign_date'],d47201.iloc[:,396:398],d47201.iloc[:,408:418]),axis = 1)
# Get pol whose term date is not all nan
polsWTerm= polsDF.dropna(subset = ['.date_plcy_trmnt_date_01','.date_plcy_trmnt_date_02','.date_plcy_trmnt_date_03','.date_plcy_trmnt_date_04','.date_plcy_trmnt_date_05'],how = 'all')
# Get pol whose term and assignment date is not nan
polsWTerm2= polsDF.dropna(subset = ['.date_plcy_trmnt_date_01','.date_plcy_trmnt_date_02','.date_plcy_trmnt_date_03','.date_plcy_trmnt_date_04','.date_plcy_trmnt_date_05','.date_agent_assign_date'],how = 'any')


# Look at head of all pol data
# Notice.date_plcy_trmnt_date_0x columns have many NaN
# - .date_agent_assign_date also has many NaNs, and if not NaN, the assign date is later than original date
polsDF.head(10)


# Look at a case term date is later than orig date:
polsWTerm.ix[1]

# Another case term date is earlier than orig date, NO SENSE:
polsWTerm.ix[7]

# Look at the difference between org and term date, appears that most org date is later than term date, NO SENSE
pd.to_datetime(polsWTerm['.date_org_plcy_date']) - pd.to_datetime(polsWTerm['.date_plcy_trmnt_date_01'])

# Look at a case term date 01 -05 non nan, but not sure how to understand it:
polsDF.ix[3515]

# A case where not fiels are NaN, but still the term date doesn't make sense
polsWTerm2.ix[285]