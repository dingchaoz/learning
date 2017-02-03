import glob
import pandas as pd
import numpy as np

def ParseAOI(xml):    
    with open(xml, 'r') as content_file:
        content = content_file.read()

    # content2 = content[1:99999999999]
    ## New ways to extract atlas score, status, included or excluded status
    res = []
    subres = []
    for w in content.split(">"):
        if "<" in w and '' != w.split("<")[0]:
            values = w.split("<")[0]
            if values.isdigit():
                res.append(subres)
                subres = []
            subres.append(values)

    # Agents included with atlas score turned on will be like:
    #['1', '0.982075496808', 'M5Z7Y4Q7PAL', 'true']
    # Agents included with atlas score turned off will be like:
    # ['3', '0.981889713969', '01PR84M4SP5', 'false']
    # Agents excluded will be like:
    # ['2','0.985812242907','OFFICE_HAS_BEEN_MARKED_EXCLUDED_BY_AGENCY','0NVWH4M4FP5','false']
    includes = [x for x in res if len(x) == 4]
    excludes =  [x for x in res if len(x) > 4][1:]
    num_trans = len([x for x in includes if x[0] == '1'])
    num_ats_on = len([x for x in includes if x[0]=='1' and x[3] == 'true'])
    num_ats_off = len([x for x in includes if x[0]=='1' and x[3] == 'false'])

    return res,includes,excludes,num_trans,num_ats_on,num_ats_off

# Analyze the includes data to aggregate to per transcation
# 1 label by transaction 
# 2 filter out atlas off transactions
# 3 Record top agent, score, an 

    ##Sth TODO: Look at agents whose atlas is on, their display order frequency count
    ## TODO: Count #number of transactions coming through per zipcode
## for each transaction the agent atlas score is on, record the actual top one agent,
# the highest score agent, number of agent
#Per zip code, # of AOI transactions where ATLAS== true, number of agents, actual ATLAS score per agent, actual conversion rate?


# def main():
#     #xml = 'listval_20170101_235902.xml'
#     # List all xml files
#     # xmlFiles = glob.glob("/san-data/atlas_id/*xml")
#     xmlFiles = glob.glob("*xml")
#     Date = []
#     Res = []
#     Includes = []
#     Excludes = []
#     Num_trans = []
#     Num_ats_on = []
#     Num_ats_off = []


#     # Parse xml files
#     for xml in xmlFiles:
#         date = xml.split('_')[1]
#         res,includes,excludes,num_trans,num_ats_on,num_ats_off = ParseAOI(xml)
#         Date.append(date)
#         Res.append(res)
#         Includes.append(includes)
#         Excludes.append(excludes)
#         Num_trans.append(num_trans)
#         Num_ats_on.append(num_ats_on)
#         Num_ats_off.append(num_ats_off)

#     df_dict = {'Date':Date,'Num':Num_trans,'Num_ats_on':Num_ats_on,'Num_ats_off':Num_ats_off
#     }

#     df = pd.DataFrame(df_dict)
#     df.to_csv('.csv')

    #return res,includes,excludes,num_trans,num_ats_on,num_ats_off

if __name__ == '__main__':
    #main()
    xmlFiles = glob.glob("*xml")
    Date = []
    #Res = []
    Includes = []
    #Excludes = []
    TopMaxAgt = []
    Num_trans = []
    Num_ats_on = []
    Num_ats_off = []


    # Parse xml files
    for xml in xmlFiles:
        date = xml.split('_')[1] # Get the date
        res,includes,excludes,num_trans,num_ats_on,num_ats_off = ParseAOI(xml) # Pasre xml
        Date.append(date) 
        #Res.append(res)

        # Construct a df to store includes
        dfincludes = pd.DataFrame(includes,columns = ['Pos','ATLS_SCORE','ASSOC_ID','ATLS_APPLIED'])
        # Include date column
        dfincludes['Date'] = date
        #dfincludes['Trans'] = None
        #dfincludes['Pos'] = pd.to_numeric(dfincludes['Pos']) # Convert Pos to numeric


        transnums = []
        # Get list of agents whose atlas score is applied
        df_on = dfincludes[dfincludes.ATLS_APPLIED == 'true']
        transnum = 1
        for i in range(1, df_on.shape[0]):
            
            if float(df_on['Pos'].iloc[i]) <= float(df_on['Pos'].iloc[i-1]):
                transnum += 1        
            transnums.append(transnum)

        transnums =  [1] + transnums
        df_on['Trans'] = transnums
        # df_on.groupby('Trans')['ATLS_SCORE'].agg('count')
        # df_on.groupby('Trans')['ATLS_SCORE'].agg(np.min)

        #idx = df_on.groupby(['Trans'])['ATLS_SCORE'].transform(max) == df_on['Trans']
        #df_MaxScoreAgent = df_on[idx]

        df_MaxScoreAgent = df_on.sort('ATLS_SCORE',ascending = False).groupby('Trans',as_index = False).first()
        df_TopAgent = df_on[df_on.Pos =='1']
        
        df_total = df_TopAgent.copy()
        df_total.columns = ['TopPos','TopScore','TopAgent','ATLS_APPLIED','Date','Trans']
        df_total['MaxSAgent'] = df_MaxScoreAgent.ASSOC_ID
        df_total['MaxScore'] = df_MaxScoreAgent.ATLS_SCORE
        df_total['MaxScorePos'] = df_MaxScoreAgent.Pos

        TopMaxAgt.append(df_total)
        
        # Append the df into a list
        #Includes.append(dfincludes)

        # Construct a df to store excludes and append to a list, run into memory issue
        # excludes_noreasons = [x[1:2]+x[-2:-1] for x in excludes]
        # excludes_reasons = [x[2:-2] for x in excludes]
        # dfexcludes = pd.DataFrame(excludes_noreasons,columns = ['ATLS_SCORE','ASSOC_ID'])
        # dfexcludes['reasons'] = excludes_reasons       
        # dfexcludes['Date'] = date * dfexcludes.shape[0]
        # Excludes.append(dfexcludes)

        # Store the num trans, on and off in a list
        Num_trans.append(num_trans)
        Num_ats_on.append(num_ats_on)
        Num_ats_off.append(num_ats_off)


    # Construct num_trans, on and off list into a df and save
    AtlCount_dict = {'Date':Date,'Num':Num_trans,'Num_ats_on':Num_ats_on,'Num_ats_off':Num_ats_off
    }
    AtlCount_df = pd.DataFrame(AtlCount_dict)
    AtlCount_df.to_csv('AtlCount201701.csv')

    # Construct top displayed and max scored agent concated pd and save to csv
    TopMaxAgt_df = pd.concat(TopMaxAgt)
    TopMaxAgt_df.to_csv('TopMaxAgt201701.csv')


    # Construct includes and excludes concated pd and save to csv
    #Excludes_df = pd.concat(Excludes)
    #Includes_df = pd.concat(Includes)
    #Excludes_df.to_csv('Excludes201701.csv')
    #Includes_df.to_csv('Includes201701.csv')

