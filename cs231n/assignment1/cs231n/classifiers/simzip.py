########
## Work directory in /san-data/usecase/agentpm/AgentProductionModel
## Script to return a 2-d encoded zip matrix using pca and tsne: zipsim_tsne_completedinfo
## and a dist matrix desribing pair-wise dist of 40339 x 40339 dim: dist.npy


## Also produces these two files for valiation purposes:
## zipsimtsne_agged.csv which is a place aggregated version 2-d encoded matrix
## and dist_agg.npy
########
import os
import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from scipy.spatial.distance import pdist, squareform
os.chdir('/san-data/usecase/agentpm/AgentProductionModel/')
zipdf = pd.read_csv('zipmerged2010-2015.csv')
zipdf_num = zipdf.iloc[:,3:] # remove zip code, city name, fips code for now

#There are 1428 columns for 2011 to 2015 demographics data
# Use PCA to reduce to 50 before using TSNE to reduce computation efficiency
pca = PCA(n_components= 50)
pcaed = pca.fit_transform(zipdf_num)

# Use TSNE to reduce to 2 dimnesions
tsne = TSNE(n_components=2,random_state = 0)
tsned = tsne.fit_transform(pcaed)

# Save tsned np array into a dataframe
tsnedf = pd.DataFrame(tsned,columns  = ['x','y'],index = None)
# Append back zip code, city name, fips code
zipsim_df= pd.concat((tsnedf,zipdf.iloc[:,:3]),axis = 1)
# Save to a csv
zipsim_df.to_csv('zipSimilarity/zipsimilarity_tsne.csv',index = None)

# save tsned file to a csv, it takes long to run the tsne


## Join with other info like state, county, coordinate to search for closest similar state
zipsim_df = pd.read_csv('zipSimilarity/zipsimilarity_tsne.csv')
zipinfo = pd.read_csv('us_postal_codes.csv')
zipsimjoined = zipsim_df.set_index('ZIP').join(zipinfo.set_index('Postal Code'))
del zipsimjoined['Unnamed: 7']
del zipsimjoined['State']
zipsimjoined.to_csv('zipsim_tsne_completedinfo',index = None)



# COMPUTE DISTANCE MATRIX and save to a matrix csv
sq_dist = squareform(pdist(np.array(zip(zipsimjoined.iloc[:,0],zipsimjoined.iloc[:,1]))))
np.save('zipSimilarity/dist',sq_dist)

# Find index of the target to be compared place, say i
# then do np.argsort(sq_dist[i,]), use the element returned since the 2nd place 


# Create functio to return most similar zip
# Aggregate by city to validate that ny == chicago more than ny == bloomington,il
# sth like this to verify that if we cluster them using kmeans, we found large cities clutered 
# in one place and we color them by category: surburban, urban, rural areas


### AGG ANALYSIS ONLY THE FOLLOWING CODES

# Read zipinfo csv which has the state, county info per zip
zipdf = pd.read_csv('zipmerged2010-2015.csv')
zipinfo = pd.read_csv('us_postal_codes.csv')
# Join with zipdf
zipdfjoined = zipdf.set_index('ZIP').join(zipinfo.set_index('Postal Code'))
# Group by state and place name and agg by sum
zipdfagged = zipdfjoined.groupby(['State','Place Name']).agg(np.sum)
# Select useful columns 
zipdfagged = zipdfagged.iloc[:,1:-3]
# Reset index
zipdfagged.reset_index(inplace = True)
# Remove state and place name for now before pca and tsne
zipdfagged_num = zipdfagged.iloc[:,2:]

pca = PCA(n_components= 50)
pcaed = pca.fit_transform(zipdfagged_num)

# Use TSNE to reduce to 2 dimnesions
tsne = TSNE(n_components=2,random_state = 0)
tsned = tsne.fit_transform(pcaed)
tsnedf_agg = pd.DataFrame(tsned,columns  = ['x','y'],index = None)
zipsim_df_agg= pd.concat((tsnedf_agg,zipdfagged.iloc[:,:2]),axis = 1)
zipsim_df_agg =  pd.concat((zipsim_df_agg,zipdfagged['CURRENT_POP.2015']),axis = 1)
zipsim_df_agg.to_csv('zipSimilarity/zipsimtsne_agged.csv',index = None)

zipsim_df_agg['size'] = ['City' if x >25000 else 'Rural' if x < 50000 else 'Surb' for x in zipsim_df_agg['CURRENT_POP.2015']]
sq_dist_agged = squareform(pdist(np.array(zip(zipsim_df_agg.iloc[:,0],zipsim_df_agg.iloc[:,1]))))
pd.DataFrame(sq_dist_agged,index = None).to_csv('zipSimilarity/zip_dist_agged.csv')