import pandas as pd
import numpy as np
from matplotlib import cm
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import recall_score, average_precision_score, f1_score
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
import seaborn as sns
import os, sys

##########################################################

## Example taken from https://github.com/iwatobipen/chemo_info/blob/42be4d98b1421022a62be2c2d92f7ac153d0e5ae/sarviztest/sarviz.py

def selectalg(model):
	if model == "logit":
		return LogisticRegression(C=0.01, solver="liblinear") 
	elif model == "svm":
		return SVC( probability=True, C=100, gamma='auto' )
	elif model == "rf":
		return RandomForestClassifier()

def assespotential(dataset, Y, prop):
		if prop == "km":
			for line in dataset["logKm"]:
				#print(line)
				if float( line ) <= -1.1:
					Y.append( 1 )
				else:
					Y.append( 0 )
			return Y
			
		elif prop == "kcat":
			for line in dataset["logKcat"]:
				if float( line ) >= 0.9:
					Y.append( 1 )
				else:
					Y.append( 0 )
			return Y
			
		elif prop == "kcatkm":
			for line in dataset["logKcatkm"]:
				if float( line ) >= 1.5: 
					Y.append( 1 )
				else:
					Y.append( 0 )
			return Y

def select_features(alg):
	if alg == "rf":
		return "features/rf_coef.txt"
	elif alg == "elasticnet":
		return "features/elastic_coef.txt"
	elif alg == "lasso":
		return "features/lasso_coef.txt"
	elif alg == "ridge":
		return "features/ridge_coef.txt"
	
def mainfunction(group, prop, val, test_prop, model, feat_list):
		## Read dataset
		dataset = pd.read_csv("ml.csv/%s._.fp.vec.%s.%s.clean.csv" % (group, prop, val))
		print(dataset.head())
		print(dataset.shape)
		
		## Read smiles
		mols = dataset["ligand"]
		
		datapoints=len(mols)

		vec_fp= dataset.iloc[:, 2:3949]
		for column in vec_fp.columns:
			vec_fp["%s" % (column)] = pd.to_numeric(vec_fp["%s" % (column)], downcast="float")
		
		# label active / non active
		Y = assespotential(dataset, [], prop)
		Y = np.asarray( Y )

		#Initialize performance scores
		recall=0
		precision=0
		fscore=0
		pos=0
		
		#We do up to 10 replicas
		for replica in range(0,10):
			
			## split data
			trainx, testx, trainy, testy = train_test_split( vec_fp, Y, test_size = test_prop )
	
			## SELECT BEST FEATURES OF THE TRAINING DATA
			### Adaptation from https://towardsdatascience.com/feature-selection-techniques-in-machine-learning-with-python-f24e7da3f36e
			##trainx with best bestfeatures
			best_trainx = trainx.loc[:, feat_list]
			best_testx = testx.loc[:, feat_list]

			#print(len(mols),len(trainx), len(trainy))
			cls = selectalg(model)
			cls.fit( best_trainx, trainy )
	
			## Predict
			res = cls.predict(best_testx)
			
			## PERFORMANCE SCORES
			recall += recall_score(testy, res, average='macro')
			precision += average_precision_score(testy, res, average='macro')
			fscore += f1_score(testy, res, average='macro')
			
			if replica == 0:
				recall0 = recall_score(testy, res, average='macro')
				precision0 = average_precision_score(testy, res, average='macro')
				fscore0 = f1_score(testy, res, average='macro')
				#print(recall0)
				#print(precision0)
				#print(fscore0)
			elif replica == 4:
				recall5 = recall/5
				precision5 = precision/5
				fscore5 = fscore/5
				#print(recall5)
				#print(precision5)
				#print(fscore5)
			elif replica == 9:
				recall10 = recall/10
				precision10 = precision/10
				fscore10 = fscore/10
				#print(recall10)
				#print(precision10)
				#print(fscore10)
		##Output
		return datapoints, recall0, precision0, fscore0, recall5, precision5, fscore5, recall10, precision10, fscore10
		
################################################################################
#PARAMETERS TO TEST
test_prop_list=[0.1,0.2,0.3]
model_list=["svm", "logit"]
grouplist=["1.1.1"] #, "2.6.1", "3.1.1", "4.1.1"]
proplist=["km", "kcat", "kcatkm"]
vallist=["mean"]

feat_sel_list = ["rf", "elasticnet", "lasso", "ridge"]


#List for dataframe
pred_results=[]

#Calculamos cada regresion
for model in model_list:
	line_pos=0
	for group in grouplist:
		for prop in proplist:
			for val in vallist:
				for test_prop in test_prop_list:
					for featsel in feat_sel_list:
						#Introduce feature lists for each methon in x condition	
						feat_file=select_features(featsel)
						with open(feat_file) as feats:
							feat_list_raw=feats.readlines()[line_pos]
						feat_cols_list=feat_list_raw[1:-1].split("', '")
						feat_list=[]
						for feat_pos in range(0,len(feat_cols_list)):
							if feat_pos==0:
								feat_cols=feat_cols_list[feat_pos][1:]
							elif feat_pos==(len(feat_cols_list)-1):
								feat_cols=feat_cols_list[feat_pos][:-2]
							else:
								feat_cols=feat_cols_list[feat_pos]
							feat_list.append(feat_cols)
						
						datapoints, recall0, precision0, fscore0, recall5, precision5, fscore5, recall10, precision10, fscore10 = mainfunction(group, prop, val,test_prop, model, feat_list)
						pred_list=[group, prop, val, model, (1-test_prop)*100, test_prop*100, datapoints, featsel, recall0, recall5, recall10, precision0, precision5, precision10, fscore0, fscore5, fscore10]
						pred_results.append(pred_list)
						
					#Increase line position for next feature
					line_pos+=1

#Introduce pred_results into a dataframe	
df = pd.DataFrame(pred_results, columns = ["EC group", "kin.prop", "sign.par", "algorithm", "\%train", "\%test", "datapoints", "feat.sel.algorithm", "recall.r0", "recall.r5", "recall.r10", "precision.r0", "precision.r5", "precision.r10", "f1score.r0", "f1score.r5", "f1score.r10"])

#print(df.head())

#From dataset to csv
df.to_csv(path_or_buf="predictions/all_pred_fp_vec_classif_1.1.1.clean.csv") 
