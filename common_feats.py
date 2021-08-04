import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
plt.switch_backend('agg')
import seaborn as sns


#####################################################

def select_features(alg):
	if alg == "rf":
		return "features/rf_coef.txt"
	elif alg == "elasticnet":
		return "features/elastic_coef.txt"
	elif alg == "lasso":
		return "features/lasso_coef.txt"
	elif alg == "ridge":
		return "features/ridge_coef.txt"
	

#####################################################
#PARAMETERS 
test_prop_list=[0.1,0.2,0.3]
grouplist=["3.1.1"] #, "2.6.1", "3.1.1", "4.1.1"]
proplist=["km", "kcat", "kcatkm"]
vallist=["mean"]
line_pos=0
algorithm_list = ["rf", "elasticnet", "lasso", "ridge"]
cont=0

#Initialize dictionary
feat_dict={}



#Create function
for group in grouplist:
	for prop in proplist:
		for val in vallist:
			for test_prop in test_prop_list:
				#Initialize list of common feats
				common_feat_abs=[]
				common_feat_rel=[]
				len_feats=[]
				
				#Introduce feature lists for each methon in x condition
				for algorithm in algorithm_list:	
					feat_file=select_features(algorithm)
					with open(feat_file) as feats:
						feat_list_raw=feats.readlines()[line_pos]
					feat_list=feat_list_raw[1:-1].split(",")
					feat_dict[algorithm]=feat_list
				
				#Count number of common feats and introduce in list
				for alg1 in algorithm_list:
					len_feats.append(len(feat_dict[alg1]))
					for alg2 in algorithm_list:
						common_count=0
						for column in feat_dict[alg1]:
							if column in feat_dict[alg2]:
								common_count+=1
						common_count_abs=common_count
						common_count_rel=common_count/len(feat_dict[alg1])
						common_feat_abs.append(common_count_abs)
						common_feat_rel.append(common_count_rel)
				
				#GRAPHS
				fig, axs = plt.subplots(3)
				fig.tight_layout(pad=2.0) #Separation betwen subplots
				
				#Transform list into a matrix
				feat_m_abs=np.array(common_feat_abs)
				feat_m_rel=np.array(common_feat_rel)
				feat_m_abs=feat_m_abs.reshape(4,4)
				feat_m_rel=feat_m_rel.reshape(4,4)
				
				#Create heatmap
				graph = sns.heatmap(feat_m_abs, xticklabels=algorithm_list, yticklabels=algorithm_list, annot=True, fmt="d", ax=axs[0])
				graph2= sns.heatmap(feat_m_rel, xticklabels=algorithm_list, yticklabels=algorithm_list, annot=True, ax=axs[1])
					
				#Barplot of lengths of features by algorithm
				print(len_feats)
				num_feat_df=pd.DataFrame({"algorithm": algorithm_list, "n.features": len_feats})
				sns.barplot(x = 'algorithm', y = 'n.features', data = num_feat_df, orient="v", ax=axs[2])	
				
				plt.savefig("features/%s._.fp.vec.%s.%s.%s.common_feat.png" % (group, prop, val, str(test_prop)), dpi=1000)
				
				#Increase line position for next feature
				line_pos+=1
			
				
