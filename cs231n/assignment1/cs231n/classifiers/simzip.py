import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

zipdf = pd.read_csv('/san-data/usecase/agentpm/AgentProductionModel/zipmerged2010-2015.csv')
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
zipsim_df.to_csv('zipsimilarity_tsne.csv',index = None)

# save tsned file to a csv, it takes long to run the tsne


## TO-DO:
zipsim_df = pd.read_csv('/san-data/usecase/agentpm/AgentProductionModel/zipsimilarity_tsne.csv')
zipinfo = pd.read_csv('/san-data/usecase/agentpm/AgentProductionModel/us_postal_codes.csv')
zipsimjoined = zipsim_df.set_index('ZIP').join(zipinfo.set_index('Postal Code'))
del zipsimjoined['Unnamed: 7']
del zipsimjoined['State']
# Create functio to return most similar zip
# Aggregate by city to validate that ny == chicago more than ny == bloomington,il
# sth like this to verify that if we cluster them using kmeans, we found large cities clutered 
# in one place and we color them by category: surburban, urban, rural areas

# Visualize
# plt.scatter(zipsim_df.iloc[:,0],zipsim_df.iloc[:,1])
# # D is the city + zip code name
# for i in xrange(D):
# 	plt.annotate(s = index[i],xy = (tsned[i,0],tsned[i,1]))
# plt.show()


## Aggregated validation of simlarity
#zipdfjoined = _num zipdfjoined.iloc[:,3:-4]

# Read zipinfo csv which has the state, county info per zip
zipinfo = pd.read_csv('/san-data/usecase/agentpm/AgentProductionModel/us_postal_codes.csv')
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

