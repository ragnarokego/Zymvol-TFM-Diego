import pandas as pd
import numpy as np

#########################

for group in ["1.1.1", "2.6.1", "3.1.1", "4.1.1"]:
	main_df = pd.read_csv("protein.csv/%s._.csv" % (group))
	del main_df["Unnamed: 0"]
	print(main_df.shape)

	fp_df = pd.read_csv("Diego_fp/%s._.fp.csv" % (group), header=None, prefix = "f")
	fp_df.columns= ["f%d" %(x) for x in range(0,2048)]
	#print(fp_df.head())
	
	vec_df = pd.read_csv("Diego_vec/%s._._vec.csv" % (group))
	del vec_df["Unnamed: 0"]
	#print(vec_df.head())
	
	main_vec=pd.concat([main_df, vec_df], axis=1)
	main_vec_fp=pd.concat([main_vec, fp_df], axis=1)
	print(main_vec_fp.shape)
	
	#Create the dataframes for each property
	del main_vec_fp["km"]
	del main_vec_fp["kcat"]
	kcatkm = main_vec_fp.dropna()
	print(kcatkm.shape)
	
	#We join all the sequences vectors and ligand fingerprints togetheir indiferently of the kinetic activity
	group_vec_fp=main_vec_fp.groupby(by=["sequence", "ligand"]).count()
	group_vec_fp.to_csv(path_or_buf="ml.csv/%s._.fp.vec.group.csv" % (group))
	
	#We use the log of the properties as we saw the distributions in log
	'''
	km['logKm']=np.log10(km['km'])
	del km["km"]
	
	kcat['logKcat']=np.log10(kcat['kcat'])
	del kcat['kcat']
	
	kcatkm['logKcatkm']=np.log10(kcatkm['kcatkm'])
	del kcatkm['kcatkm']
	'''
	'''
	km_m=km.groupby(by=["sequence", "ligand"]).mean()
	del km_m['reference']
	print(km_m.shape)
	km_m.to_csv(path_or_buf="ml.csv/%s._.fp.vec.km.mean.csv" % (group))
	
	
	kcat_m=kcat.groupby(by=["sequence", "ligand"]).mean()
	del kcat_m['reference']
	print(kcat_m.shape)
	kcat_m.to_csv(path_or_buf="ml.csv/%s._.fp.vec.kcat.mean.csv" % (group))
	
	kcatkm_m=kcatkm.groupby(by=["sequence", "ligand"]).mean()
	del kcatkm_m['reference']
	print(kcatkm_m.shape)
	kcatkm_m.to_csv(path_or_buf="ml.csv/%s._.fp.vec.kcatkm.mean.csv" % (group))
	'''
