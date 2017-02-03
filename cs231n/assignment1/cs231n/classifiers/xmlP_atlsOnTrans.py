import glob
import pandas as pd
import numpy as np
import os.path

def ParseAOI(xml):    
    with open(xml, 'r') as content_file:
        content = content_file.read()

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

    includes = [x for x in res if len(x) == 4]
    excludes =  [x for x in res if len(x) > 4][1:]
    num_trans = len([x for x in includes if x[0] == '1'])
    num_ats_on = len([x for x in includes if x[0]=='1' and x[3] == 'true'])
    num_ats_off = len([x for x in includes if x[0]=='1' and x[3] == 'false'])

    return res,includes,excludes,num_trans,num_ats_on,num_ats_off

if __name__ == '__main__':
    #main()
    xmlFiles = glob.glob("*xml")

    save_path = 'ontrans/'
    # Parse xml files
    for xml in xmlFiles:

        date = xml.split('_')[1] # Get the date

        res,includes,excludes,num_trans,num_ats_on,num_ats_off = ParseAOI(xml) # Pasre xml

        # Construct a df to store includes
        dfincludes = pd.DataFrame(includes,columns = ['Pos','ATLS_SCORE','ASSOC_ID','ATLS_APPLIED'])
        # Include date column
        dfincludes['Date'] = date



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

        #Save the atlas-on-transaction data to csv
        filename = 'atlsOnTrans' + date + '.csv'
        compfilename = os.path.join(save_path,filename )
        df_on.to_csv(compfilename,index = None)

        print 'saved file: ' + filename
        


