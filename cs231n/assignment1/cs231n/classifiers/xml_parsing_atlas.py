#from collections import Counter

# def getAgentList(xml):
#     with open(xml, 'r') as content_file:
#         content = content_file.read()
#     #When file is large
#     content = content[1:2000]
#     includedAgents = []
#     excludedAgents = []
#     num_trans = len(content.split('<transactionID>')) - 2
#     for i in range(1,num_trans):
#         try: 
#             # The following works for old 2015 xml file only
#             # includedAgent = [x.split('</officeAssociateID>')[0] \
#             #              for x in content.split('<transactionID>')\
#             #              [i].split('<includedOffices><officeAssociateID>')]\
#             #              [1:]
#             includedAgents.append(includedAgent)
#         except:
#             pass
#         try:
#             # The following works for old 2015 xml file only
#             # excludedAgent = [[x.split('</officeAssociateID>')[0],\
#             #                   x.split('</officeAssociateID>')[1].\
#             #                   split('>')[1].replace('</removalReasons','')]\
#             #                  for x in content.split('<transactionID>')\
#             #                  [i].split('<removedOffices><officeAssociateID>')]\
#             #                  [1:]
#             excludedAgents.append(excludedAgent)
#         except:
#             pass
#     return includedAgents,excludedAgents

import glob
import pandas as pd

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


    ##Sth TODO: Look at agents whose atlas is on, their display order frequency count
    ## TODO: Count #number of transactions coming through per zipcode
## for each transaction the agent atlas score is on, record the actual top one agent,
# the highest score agent, number of agent
#Per zip code, # of AOI transactions where ATLAS== true, number of agents, actual ATLAS score per agent, actual conversion rate?
def main():
    #xml = 'listval_20170101_235902.xml'
    # List all xml files
    xmlFiles = glob.glob("/san-data/atlas_id/*xml")
    Date = []
    Res = []
    Includes = []
    Excludes = []
    Num_trans = []
    Num_ats_on = []
    Num_ats_off = []


    # Parse xml files
    for xml in xmlFiles:
        date = xml.split('_')[1]
        res,includes,excludes,num_trans,num_ats_on,num_ats_off = ParseAOI(xml)
        Date.append(date)
        Res.append(res)
        Includes.append(includes)
        Excludes.append(excludes)
        Num_trans.append(num_trans)
        Num_ats_on.append(num_ats_on)
        Num_ats_off.append(num_ats_off)

    df_dict = {'Date':Date,'Num':Num_trans,'Num_ats_on':Num_ats_on,'Num_ats_off':Num_ats_off
    }

    df = pd.DataFrame(df_dict)
    df.to_csv('testRes.csv')

    #return res,includes,excludes,num_trans,num_ats_on,num_ats_off

if __name__ == '__main__':
    main()
    # xml = 'listval_20170101_235902.xml'
    # res,includes,excludes,num_trans,num_ats_on,num_ats_off = ParseAOI(xml)
    # return res,includes,excludes,num_trans,num_ats_on,num_ats_off
    #print 1,2,3

    # includes,excludes = getAgentList('listval_20170101_235902.xml')
    # # Index the list to show order of display
    # includes_indexed = [[(x,y.index(x)) for x in y] for  y in includes]

    # # Flatten the list
    # includes_flattened = [item for sublist in includes_indexed for item in sublist]
    # excludes_flattened = [item for sublist in excludes for item in sublist]

    # # Show the most common 50 agents and their appearing order 
    # Counter(includes_flattened).most_common(50)

    # #<atlasScoreApplied>true
    # #<officePosition>5</officePosition>