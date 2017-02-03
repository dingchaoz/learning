import glob
import pandas as pd
import numpy as np
import os.path



if __name__ == '__main__':
    
    csvFiles = glob.glob("ontrans/atlsOnTrans2017*csv")
    TopMaxAgt = []
    save_path = 'ontrans/'

    # Read csv files
    for csv in csvFiles:
        date = csv.split('ontrans/atlsOnTrans')[1][:8] # Get the date

        df_on = pd.read_csv(csv)
        df_MaxScoreAgent = df_on.sort('ATLS_SCORE',ascending = False).groupby('Trans',as_index = False).first()
        df_TopAgent = df_on[df_on.Pos == 1]
        
        df_TopAgent.columns = ['TopPos','TopScore','TopAgent','ATLS_APPLIED','Date','Trans']
        del df_MaxScoreAgent['Date']
        del df_MaxScoreAgent['ATLS_APPLIED']
        df_MaxScoreAgent.columns = ['Trans','MaxScorePos','MaxScore','MaxAgent']
        df_total = pd.merge(df_TopAgent,df_MaxScoreAgent,on = 'Trans')

        TopMaxAgt.append(df_total)
        print 'Extracted top and max agents on this date: ' +  date

    # Construct top displayed and max scored agent concated pd and save to csv
    TopMaxAgt_df = pd.concat(TopMaxAgt)
    #Save the atlas-on-transaction data to csv
    filename = 'TopMaxAgt201701.csv'
    compfilename = os.path.join(save_path,filename )
    TopMaxAgt_df.to_csv(compfilename,index = None)

    print 'Extractions on all files completed, saved as: ' + filename



