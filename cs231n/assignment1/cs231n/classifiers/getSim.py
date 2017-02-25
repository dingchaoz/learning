########

## Script to take in a target place, and return most similar demographic places

########


import pandas as pd
import numpy as np
import os
import glob
from scipy.spatial.distance import pdist, squareform

# Set up working directory
os.chdir('/san-data/usecase/agentpm/AgentProductionModel/zipSimilarity')
# Load zip distance pair-wise matrix
sq_dist = np.load('dist.npy')
# Load zip 2d encoded matrix
zipsim = pd.read_csv('zipsim_tsne_completedinfo')
## Load zip distance pair-wise matrix
sq_distagged = np.load('dist_agg.npy')
# Load zip 2d encoded matrix
zipsimagged = pd.read_csv('zipsimtsne_agged.csv')


def getSimilarAgged(place):
	 idx = zipsimagged[zipsimagged['Place Name']==Place].index.tolist()[0]
	 return zipsimagged.ix[np.argsort(sq_distagged[idx,])[:30]]['Place Name']