import pandas as pd
import seaborn as sns
import math
import numpy as np
import time
import datetime
from sklearn import metrics
import matplotlib.pyplot as plt
from spc import *
# %matplotlib inline

pd.options.display.max_columns = 100
pd.options.display.max_rows = 500

#####
#NOTE:
#The following lines construct the initial df_final which has from 20161-11's actual vs
#atlas score columns
#no need to rerun the construction process, but just append new columns for new months
#in the future

#####

jan = pd.read_csv('/san-data/usecase/atlasid/new_data/output_file/jan_time_series_scores.csv')
feb = pd.read_csv('/san-data/usecase/atlasid/new_data/output_file/feb_time_series_scores.csv')
march = pd.read_csv('/san-data/usecase/atlasid/new_data/output_file/mar_time_series_scores.csv')
april = pd.read_csv('/san-data/usecase/atlasid/new_data/output_file/apr_time_series_scores.csv')
may = pd.read_csv('/san-data/usecase/atlasid/new_data/output_file/may_time_series_scores.csv')
june = pd.read_csv('/san-data/usecase/atlasid/new_data/output_file/jun_time_series_scores.csv')
july = pd.read_csv('/san-data/usecase/atlasid/new_data/output_file/jul_time_series_scores.csv')
aug = pd.read_csv('/san-data/usecase/atlasid/new_data/output_file/aug_time_series_scores.csv')
sep = pd.read_csv('/san-data/usecase/atlasid/new_data/output_file/sep_time_series_scores.csv')
oct = pd.read_csv('/san-data/usecase/atlasid/new_data/output_file/oct_time_series_scores.csv')
nov = pd.read_csv('/san-data/usecase/atlasid/new_data/output_file/nov_time_series_scores.csv')

atlas = pd.read_csv('/san-data/usecase/atlasid/new_data/csv/atlas_time_series.csv')

jan = jan[jan.CSE_RSLT_IND == 1][['ASSOC_ID','score']]
feb = feb[feb.CSE_RSLT_IND == 1][['ASSOC_ID','score']]
march = march[march.CSE_RSLT_IND == 1][['ASSOC_ID','score']]
april = april[april.CSE_RSLT_IND == 1][['ASSOC_ID','score']]
may = may[may.CSE_RSLT_IND == 1][['ASSOC_ID','old_score']]
june = june[june.CSE_RSLT_IND == 1][['ASSOC_ID','score']]
july = july[july.CSE_RSLT_IND == 1][['ASSOC_ID','score']]
aug = aug[aug.CSE_RSLT_IND == 1][['ASSOC_ID','score']]
sep = sep[sep.CSE_RSLT_IND == 1][['ASSOC_ID','old_score']]
oct = aug[oct.CSE_RSLT_IND == 1][['ASSOC_ID','score']]
nov = sep[nov.CSE_RSLT_IND == 1][['ASSOC_ID','old_score']]


atlas = atlas[atlas.CSE_RSLT_IND == 1]
atlas_jan = atlas[atlas.QUOT_MONTH_new == '2016-01-01'][['ASSOC_ID','CONV_RATE']]
atlas_feb = atlas[atlas.QUOT_MONTH_new == '2016-02-01'][['ASSOC_ID','CONV_RATE']]
atlas_march = atlas[atlas.QUOT_MONTH_new == '2016-03-01'][['ASSOC_ID','CONV_RATE']]
atlas_april = atlas[atlas.QUOT_MONTH_new == '2016-04-01'][['ASSOC_ID','CONV_RATE']]
atlas_may = atlas[atlas.QUOT_MONTH_new == '2016-05-01'][['ASSOC_ID','CONV_RATE']]
atlas_june = atlas[atlas.QUOT_MONTH_new == '2016-06-01'][['ASSOC_ID','CONV_RATE']]
atlas_july = atlas[atlas.QUOT_MONTH_new == '2016-07-01'][['ASSOC_ID','CONV_RATE']]
atlas_aug = atlas[atlas.QUOT_MONTH_new == '2016-08-01'][['ASSOC_ID','CONV_RATE']]
atlas_sep = atlas[atlas.QUOT_MONTH_new == '2016-09-01'][['ASSOC_ID','CONV_RATE']]
atlas_oct = atlas[atlas.QUOT_MONTH_new == '2016-09-01'][['ASSOC_ID','CONV_RATE']]
atlas_nov = atlas[atlas.QUOT_MONTH_new == '2016-10-01'][['ASSOC_ID','CONV_RATE']]

#Merge all data frames and compute forecast error monthly, the new data frame is called df_final
dfs = [atlas_jan,atlas_feb,atlas_march,atlas_april,atlas_may,atlas_june,atlas_july,atlas_aug,atlas_sep,atlas_oct,atlas_nov,jan,feb,march,april,may,june,july,aug,sep,oct,nov]
df_final = reduce(lambda left,right: pd.merge(left,right,on='ASSOC_ID'), dfs)

conv_cols = ['CONV_RATE_2016'+ str(i) for i in range(1,12)]
score_cols = ['SCORE_2016'+ str(i) for i in range(1,12)]
cols = ['ASSOC_ID'] + conv_cols + score_cols
df_final.columns = cols

for i in range(1,12):
    df_final['ERR_2016'+str(i)] = df_final['CONV_RATE_2016'+str(i)] - df_final['SCORE_2016'+str(i)]
# Save into a csv file
df_final.to_csv('/san-data/usecase/atlasid/new_data/output_file/ts_actual_forecast_20161-11.csv')


######
# End of initial file construction
######