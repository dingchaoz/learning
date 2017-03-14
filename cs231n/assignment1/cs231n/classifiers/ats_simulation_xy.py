"""
VARIABLE SETS VALUE UNKNOW, VALUES NEED TO BE MANUALLY SET
"""

MICRO_SITE_PERC = 0.02 #VARIABLE 1

FINISHING_PERC = 0.46 # VARIABLE 2 great idea looking into shoppers data + aoi

#VARIABLE SET 3
AGENT1_SELECT_PERC = 1
AGENT2_SELECT_PERC = 0
AGENT3_SELECT_PERC = 1 - AGENT2_SELECT_PERC - AGENT1_SELECT_PERC

"""
VARIABLES VALUE KNOWN ALREADY
"""
total_new_pols = 30142
total_trans = 498924
agent1_current_avg_conv = 0.13
agent2_current_avg_conv = 0.13
agent3_current_avg_conv = 0.13

agent1_atlas_avg_conv = 0.16
agent2_atlas_avg_conv = 0.13
agent3_atlas_avg_conv = 0.13

# agent1_atlas_avg_conv = 0.1396
# agent2_atlas_avg_conv = 0.1349
# agent3_atlas_avg_conv = 0.13



"""
FORMULAS
"""
#DERIVED FORMULA
FINISHING_PERC = total_new_pols * (1 - MICRO_SITE_PERC) / (total_trans * \
				(AGENT1_SELECT_PERC * agent1_current_avg_conv + \
				AGENT2_SELECT_PERC * agent2_current_avg_conv + \
				AGENT3_SELECT_PERC * agent3_current_avg_conv))

sfcom_new_pols = total_new_pols * (1 - MICRO_SITE_PERC) #FORMULA 1

microsite_new_pols = total_new_pols * MICRO_SITE_PERC #FORMULA 2

total_leads = total_trans * FINISHING_PERC #FORMULA 3 -- need to double check the shoppers

# FORMULA 4
sfcom_new_pols = total_leads * (\
				AGENT1_SELECT_PERC* agent1_current_avg_conv + \
				AGENT2_SELECT_PERC * agent2_current_avg_conv + \
				AGENT3_SELECT_PERC * agent3_current_avg_conv)

#FORMULA 5
sfcom_new_pols_atlas = total_leads * (\
				AGENT1_SELECT_PERC * agent1_atlas_avg_conv + \
				AGENT2_SELECT_PERC * agent2_atlas_avg_conv + \
				AGENT3_SELECT_PERC * agent3_atlas_avg_conv)

#FORMULA 6
gain_new_pols = sfcom_new_pols_atlas - sfcom_new_pols
print gain_new_pols

"""
# gain_new_pols = total_leads * agent1_select_perc * \
# (agent1_atlas_avg_conv - agent1_current_avg_conv)
total_new_pols * (1 - micro_site_perc) = /
total_leads * agent1_select_perc * agent1_current_avg_conv = /
total_trans * finishing_perc * agent1_select_perc * agent1_current_avg_conv
==>
finishing_perc = total_new_pols * (1 - micro_site_perc) / (total_trans * agent1_select_perc * agent1_current_avg_conv)
"""

"""
randomFactor == 1
"""

"""
SMALLEST GAIN SCENARIO:
MICRO_SITE_PERC =  0.9
AGENT1_SELECT_PERC = 0.33
AGENT2_SELECT_PERC = 0.33
AGENT3_SELECT_PERC = 0.33
"""

# gain_new_pols = 309
# random factor ==2: 112

"""
LARGEST GAIN SCENARIO:
MICRO_SITE_PERC = 0
AGENT1_SELECT_PERC = 1
AGENT2_SELECT_PERC = 0
AGENT3_SELECT_PERC = 0
"""
# gain_new_pols = 6955
# random factor ==2: 2225

"""
MOST LIKELY GAIN SCENARIO:
MICRO_SITE_PERC = 0.02
AGENT1_SELECT_PERC = 0.8
AGENT2_SELECT_PERC = 0.1
AGENT3_SELECT_PERC = 0.1
"""

# gain_new_pols = 5680
# random factor ==2: 1894


"""
recompute conv rate using random factor
randomFactor be a float input
"""

def conv_Randed(orgConv,randomFactor):
	randomed = [x ** (1/randomFactor) for x in orgConv]
	sum_randomed = sum(randomed)
	randomed_normed = [x/sum_randomed for x in randomed]
	ratio = [x/randomed_normed[-1] for x in randomed_normed]
	new_conv = [x*orgConv[-1] for x in ratio]
	return new_conv


