import os
import pandas as pd
import numpy as np
import cPickle as pickle
import collections

os.chdir('/san-data/usecase/agentpm/AgentProductionModel/')

# Read the file has each agents' home zip and top 10 pols zips
dfRes = pd.read_pickle('radiusAnalysis/radiusZips')

## Count how many agents got top 10 - 1 zips returned:
c = collections.Counter([len(x)/9 for x in dfRes.TOP10ZIPS])
# Counter({1: 73,
#          2: 113,
#          3: 115,
#          4: 159,
#          5: 235,
#          6: 257,
#          7: 348,
#          8: 425,
#          9: 498,
#          10: 15738})


# expand df.TOP10ZIPS into its own dataframe
tags = dfRes['TOP10ZIPS'].apply(pd.Series)

# rename each variable is tags
tags = tags.rename(columns = lambda x : 'zip_' + str(x))

# view the tags dataframe
#tags

# Merge dfRes and expanded zip tags
dfResExpanded = pd.concat([dfRes,tags],axis = 1)
# remove the old column with zips in a list
dfResExpanded.drop('TOP10ZIPS',inplace = True,axis = 1)
# correct the index of the pd
dfResExpanded = dfResExpanded.set_index([range(dfResExpanded.shape[0])])
# dfResExpanded.head()
# Good to see that home zip is not the top 1 zip produces most pols in many cases

# Check if all home zips are digits(US), there are some of them are not
all([str(x).isdigit() for x in dfResExpanded.HOMEZIP])

# Get the row index of canada agents
canadaIndex = [i for (i,x) in enumerate(dfResExpanded.HOMEZIP) if not str(x).isdigit()]
# Remove canadian records
dfResExpanded.drop(dfResExpanded.index[canadaIndex],inplace = True)

# Read the latest available demographics data, the columns actuall have up to previous 8 years of pol related data,
# so no need to use previous demogrphics zip data
# Change the num_year of the file to produce different years of zip features
dfDem = pd.read_csv('/san-data/usecase/agentpm/Demographics/zpmerge_2010.csv')
# Remove all ethnic columns
dfDem.drop(dfDem.filter(regex = 'ETHNIC').columns,axis = 1,inplace = True)

##TO-do: use PLS directly on the prediction, other than PCA then linear regression
## : join each top zip to the demographics features, and then concate all together, maybe the quickest way to
## create features

# zip_0 to zip_9 are all strings so convert the following cols to str too before merging
dfDem['ZIP'] = dfDem.ZIP.astype(str)
#dfResExpanded['HOMEZIP'] = dfResExpanded['HOMEZIP'].astype(str)

##Merge on the zips
homezipMerged = dfResExpanded.merge(dfDem,left_on = 'HOMEZIP',right_on = 'ZIP',how = 'left')
zip0Merged = dfResExpanded.merge(dfDem,left_on = 'zip_0',right_on = 'ZIP',how = 'left')
zip1Merged = dfResExpanded.merge(dfDem,left_on = 'zip_1',right_on = 'ZIP',how = 'left')
zip2Merged = dfResExpanded.merge(dfDem,left_on = 'zip_2',right_on = 'ZIP',how = 'left')
zip3Merged = dfResExpanded.merge(dfDem,left_on = 'zip_3',right_on = 'ZIP',how = 'left')
zip4Merged = dfResExpanded.merge(dfDem,left_on = 'zip_4',right_on = 'ZIP',how = 'left')
zip5Merged = dfResExpanded.merge(dfDem,left_on = 'zip_5',right_on = 'ZIP',how = 'left')
zip6Merged = dfResExpanded.merge(dfDem,left_on = 'zip_6',right_on = 'ZIP',how = 'left')
zip7Merged = dfResExpanded.merge(dfDem,left_on = 'zip_7',right_on = 'ZIP',how = 'left')
zip8Merged = dfResExpanded.merge(dfDem,left_on = 'zip_8',right_on = 'ZIP',how = 'left')
zip9Merged = dfResExpanded.merge(dfDem,left_on = 'zip_9',right_on = 'ZIP',how = 'left')


# Drop duplicate columns and add zip prefix so we know which features are from which zip prior to merge all
zip0Merged.drop(zip0Merged.columns[range(15)],axis=1,inplace=True)
zip0Merged.columns = ['zip0_'+ x for x in zip0Merged.columns]
zip1Merged.drop(zip1Merged.columns[range(15)],axis=1,inplace=True)
zip1Merged.columns = ['zip1_'+ x for x in zip1Merged.columns]
zip2Merged.drop(zip2Merged.columns[range(15)],axis=1,inplace=True)
zip2Merged.columns = ['zip2_'+ x for x in zip2Merged.columns]
zip3Merged.drop(zip3Merged.columns[range(15)],axis=1,inplace=True)
zip3Merged.columns = ['zip3_'+ x for x in zip3Merged.columns]
zip4Merged.drop(zip4Merged.columns[range(15)],axis=1,inplace=True)
zip4Merged.columns = ['zip4_'+ x for x in zip4Merged.columns]
zip5Merged.drop(zip5Merged.columns[range(15)],axis=1,inplace=True)
zip5Merged.columns = ['zip5_'+ x for x in zip5Merged.columns]
zip6Merged.drop(zip6Merged.columns[range(15)],axis=1,inplace=True)
zip6Merged.columns = ['zip6_'+ x for x in zip6Merged.columns]
zip7Merged.drop(zip7Merged.columns[range(15)],axis=1,inplace=True)
zip7Merged.columns = ['zip7_'+ x for x in zip7Merged.columns]
zip8Merged.drop(zip8Merged.columns[range(15)],axis=1,inplace=True)
zip8Merged.columns = ['zip8_'+ x for x in zip8Merged.columns]
zip9Merged.drop(zip9Merged.columns[range(15)],axis=1,inplace=True)
zip9Merged.columns = ['zip9_'+ x for x in zip9Merged.columns]

## Concate all features and zips
dfZipFeatures = pd.concat([homezipMerged,zip0Merged,zip1Merged,zip2Merged,zip3Merged,zip4Merged,zip5Merged,zip6Merged,zip7Merged,zip8Merged,zip9Merged],axis = 1)


dfZipFeatures.to_csv('top10ZipFeatures/top10ZipFeatures_2010.csv',index = None)
dfZipFeatures.to_pickle('top10ZipFeatures/top10ZipFeatures_2010')