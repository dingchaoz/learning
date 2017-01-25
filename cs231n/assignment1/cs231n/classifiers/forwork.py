from collections import Counter

def getAgentList(xml):
    with open(xml, 'r') as content_file:
        content = content_file.read()
    #When file is large
    content = content[1:2000]
    includedAgents = []
    excludedAgents = []
    num_trans = len(content.split('<transactionID>')) - 2
    for i in range(1,num_trans):
        try: 
            # The following works for old 2015 xml file only
            # includedAgent = [x.split('</officeAssociateID>')[0] \
            #              for x in content.split('<transactionID>')\
            #              [i].split('<includedOffices><officeAssociateID>')]\
            #              [1:]
            includedAgents.append(includedAgent)
        except:
            pass
        try:
            # The following works for old 2015 xml file only
            # excludedAgent = [[x.split('</officeAssociateID>')[0],\
            #                   x.split('</officeAssociateID>')[1].\
            #                   split('>')[1].replace('</removalReasons','')]\
            #                  for x in content.split('<transactionID>')\
            #                  [i].split('<removedOffices><officeAssociateID>')]\
            #                  [1:]
            excludedAgents.append(excludedAgent)
        except:
            pass
    return includedAgents,excludedAgents
    
    includes,excludes = getAgentList('listval_20170101_235902.xml')
    # Index the list to show order of display
    includes_indexed = [[(x,y.index(x)) for x in y] for  y in includes]

    # Flatten the list
    includes_flattened = [item for sublist in includes_indexed for item in sublist]
    excludes_flattened = [item for sublist in excludes for item in sublist]

    # Show the most common 50 agents and their appearing order 
    Counter(includes_flattened).most_common(50

    #<atlasScoreApplied>true
    #<officePosition>5</officePosition>