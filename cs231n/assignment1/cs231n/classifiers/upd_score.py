import glob
import pandas as pd
import numpy as np
import os


if __name__ == '__main__':

	os.chdir('/san-data/atlas_id/')
	novScore = pd.read_csv('nov_time_series_scores.csv')
	novScore = novScore[['ASSOC_ID','score']]
	novScore['ASSOC_ID'] =  novScore['ASSOC_ID'].astype(str)

	csvFiles = glob.glob("ontrans/atlsOnTrans2017*csv")
	agtOfficeFile = 'logs/agent_select_score_log_file.txt'
	save_path = 'ontrans/'
	agtOfficeDF = pd.read_csv(agtOfficeFile,sep = '|')
	agtOfficeDF=agtOfficeDF.rename(columns = {'AGT_ASSOC_ID':'ASSOC_ID'})
	novScoreMerged = novScore.merge(agtOfficeDF,on = 'ASSOC_ID',how = 'left')
	TopMaxAgt = []

	for csv in csvFiles:

    	date = csv.split('ontrans/atlsOnTrans')[1][:8] # Get the date
    	df_on_raw = pd.read_csv(csv)
    	df_on_raw=df_on_raw.rename(columns = {'ASSOC_ID':'#OFFC_ASSOC_ID'})
        # Works now
        df_on = df_on_raw.merge(novScoreMerged,on = '#OFFC_ASSOC_ID',how = 'left')
        del df_on['ATLS_SCORE']
        del df_on['#OFFC_ASSOC_ID']
        del df_on['ATLS_APPLIED']
        del df_on['TERRITORY']
        del df_on['SCORE']
        del df_on['SHUFFLE_PARM']
        del df_on['AVERAGE_SCORE']
        del df_on['FINAL_SCORE']
        del df_on['ACTN_CD']
        
        df_MaxScoreAgent = df_on.sort('score',ascending = False).groupby('Trans',as_index = False).first()
        df_TopAgent = df_on[df_on.Pos == 1]
        
        #df_TopAgent.columns = ['TopPos','TopScore','TopAgent','ATLS_APPLIED','Date','Trans']
        df_TopAgent=df_TopAgent.rename(columns = {'Pos':'TopPos','score':'TopScore','ASSOC_ID':'TopAgent'})

        del df_MaxScoreAgent['Date']
        df_MaxScoreAgent.columns = ['Trans','MaxScorePos','MaxAgent','MaxScore']
        #df_total = pd.merge(df_TopAgent,df_MaxScoreAgent,on = 'Trans')
        df_total = df_TopAgent.merge(df_MaxScoreAgent,on = 'Trans').sort('Trans')

        TopMaxAgt.append(df_total)
        print 'Extracted top and max agents on this date: ' +  date

    # Construct top displayed and max scored agent concated pd and save to csv
    TopMaxAgt_df = pd.concat(TopMaxAgt)
    #Save the atlas-on-transaction data to csv
    filename = 'TopMaxAgt201701.csv'
    compfilename = os.path.join(save_path,filename )
    TopMaxAgt_df.to_csv(compfilename,index = None)
    print 'Extractions on all files completed, saved as: ' + filename




    ####
    # Update random factor part
    ####
score = [0.15,0.1,0.1,0.25,0.8,0.2]
# fairness factor == 2
score_trans = [pow(x,0.5) for x in score]
sum_transcore = sum(score_trans)
score_trans_normed = [x/sum_transcore for x in score_trans]





        
