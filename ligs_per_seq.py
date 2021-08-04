import pandas as pd
from pymongo import MongoClient
import matplotlib.pyplot as plt
import seaborn as sns 
from tabulate import tabulate

###################################################################################################################

def _connect_mongo(host, port, username, password, db):
    """ A util for making a connection to mongo """

    if username and password:
        mongo_uri = 'mongodb://%s:%s@%s:%s/%s' % (username, password, host, port, db)
        conn = MongoClient(mongo_uri)
    else:
        conn = MongoClient(host, port)

    return conn[db]


def read_mongo(db, collection, query, host='localhost', port=27017, username=None, password=None, no_id=True):
    """ Read from Mongo and Store into DataFrame """

    # Connect to MongoDB
    db = _connect_mongo(host=host, port=port, username=username, password=password, db=db)

    # Make a query to the specific DB and Collection
    cursor = db[collection].aggregate(query)
	
    #print(cursor)
    
    # Expand the cursor and construct the DataFrame
    df =  pd.DataFrame(list(cursor))

    # Delete the _id
    #if no_id:
        #del df['_id']

    return df
    
################################################################################################################### 
    
###### PROGRAM

db= "Zymvol_DRR_2021"

collection= "enzyme"

#QUERIES IN THE MONGO DATABASE
pipeline_km = [ {"$match": {"_cls": "km", "ecNumber": {"$regex": "^3.1.1.", "$options": "i"}, "firstAccessionCode": {"$exists": 1, "$not": {"$regex": "Multiple", "$options": "i"} }}}, {"$group": {"_id": {"sequences": "$firstAccessionCode", "substrate": "$ligandStructureId"}}}, {"$group": {"_id": {"sequence": "$_id.sequences"}, "total": {"$sum": 1}}}, {"$project": {"sequence": "$_id.sequence", "total": "$total", "_id": 0}}, {"$sort": {"sequence": 1}}, {"$limit": 1000 } ]

pipeline_kcatkm = [ {"$match": {"_cls": "kcatkm", "ecNumber": {"$regex": "^3.1.1.", "$options": "i"}, "firstAccessionCode": {"$exists": 1, "$not": {"$regex": "Multiple", "$options": "i"} }}}, {"$group": {"_id": {"sequences": "$firstAccessionCode", "substrate": "$ligandStructureId"}}}, {"$group": {"_id": {"sequence": "$_id.sequences"}, "total": {"$sum": 1}}}, {"$project": {"sequence": "$_id.sequence", "total": "$total", "_id": 0}}, {"$sort": {"sequence": 1}}, {"$limit": 1000 } ]

pipeline_turnnum = [ {"$match": {"_cls": "turnnum", "ecNumber": {"$regex": "^3.1.1.", "$options": "i"}, "firstAccessionCode": {"$exists": 1, "$not": {"$regex": "Multiple", "$options": "i"} }}}, {"$group": {"_id": {"sequences": "$firstAccessionCode", "substrate": "$ligandStructureId"}}}, {"$group": {"_id": {"sequence": "$_id.sequences"}, "total": {"$sum": 1}}}, {"$project": {"sequence": "$_id.sequence", "total": "$total", "_id": 0}}, {"$sort": {"sequence": 1}}, {"$limit": 1000 } ]

#CREATE THE DATAFRAMES
df_km = read_mongo(db, collection, pipeline_km, host='localhost', port=27017, username=None, password=None, no_id=True).sort_values(["total"], ascending=False)
df_kcatkm = read_mongo(db, collection, pipeline_kcatkm, host='localhost', port=27017, username=None, password=None, no_id=True).sort_values(["total"], ascending=False)
df_turnnum = read_mongo(db, collection, pipeline_turnnum, host='localhost', port=27017, username=None, password=None, no_id=True).sort_values(["total"], ascending=False)


#print(df_km.head())
print(df_km.shape)

#CREATE THE BARPLOTS

#Bar graph for km
plt.bar(df_km.sequence, df_km.total, width=0.4, bottom=None, align='center', color= "red")
plt.title("3.1.1.* km", fontsize=18)
plt.tick_params(
    axis='x',          
    which='major',
    bottom=False,  
    top=False, 
    labelbottom=False)
plt.xlabel("Sequences", fontsize=16)
plt.ylabel("Substrates per sequence", fontsize=16)
plt.yticks(fontsize=16)
plt.savefig("./Resultados_9_6_2021/Graphs/3.1.1.*_km_substrate_seq.png", dpi=1000)

#Bar graph for kcatkm
plt.bar(df_kcatkm.sequence, df_kcatkm.total, width=0.4, bottom=None, align='center', color= "red")
plt.title("3.1.1.* kcatkm", fontsize=18)
plt.xlabel("Sequences", fontsize=16)
plt.ylabel("Substrates per sequence", fontsize=16)
plt.tick_params(
    axis='x',          
    which='major',
    bottom=False,  
    top=False, 
    labelbottom=False)
plt.yticks(fontsize=16)
plt.savefig("./Resultados_9_6_2021/Graphs/3.1.1.*_kcatkm_substrate_seq.png", dpi=1000)

#Bar graph for turnnum
plt.bar(df_turnnum.sequence, df_turnnum.total, width=0.4, bottom=None, align='center', color= "red")
plt.title("3.1.1.* kcat", fontsize=18)
plt.xlabel("Sequences", fontsize=16)
plt.ylabel("Substrates per sequence", fontsize=16)
plt.tick_params(
    axis='x',          
    which='major',
    bottom=False,  
    top=False, 
    labelbottom=False)
plt.yticks(fontsize=16)
plt.savefig("./Resultados_9_6_2021/Graphs/3.1.1.*_kcat_substrate_seq.png", dpi=1000)

##############################

pipeline2_km = [ {"$match": {"_cls": "km", "ecNumber": {"$regex": "^3.1.1.", "$options": "i"}, "firstAccessionCode": {"$exists": 1, "$not": {"$regex": "Multiple", "$options": "i"} }}}, {"$group": {"_id": { "ecNumber": "$ecNumber", "sequences": "$firstAccessionCode", "substrate": "$ligandStructureId"}, "total": {"$sum": 1}}}, {"$project": {"ecNumber": "$_id.ecNumber", "sequence": "$_id.sequences", "substrate": "$_id.substrate", "total": "$total", "_id": 0}}, {"$sort": {"ecNumber": 1}}, {"$limit": 100000 } ]
pipeline2_kcatkm = [ {"$match": {"_cls": "kcatkm", "ecNumber": {"$regex": "^3.1.1.", "$options": "i"}, "firstAccessionCode": {"$exists": 1, "$not": {"$regex": "Multiple", "$options": "i"} }}}, {"$group": {"_id": { "ecNumber": "$ecNumber", "sequences": "$firstAccessionCode", "substrate": "$ligandStructureId"}, "total": {"$sum": 1}}}, {"$project": {"ecNumber": "$_id.ecNumber", "sequence": "$_id.sequences", "substrate": "$_id.substrate", "total": "$total", "_id": 0}}, {"$sort": {"ecNumber": 1}}, {"$limit": 100000 } ]
pipeline2_turnnum = [ {"$match": {"_cls": "turnnum", "ecNumber": {"$regex": "^3.1.1.", "$options": "i"}, "firstAccessionCode": {"$exists": 1, "$not": {"$regex": "Multiple", "$options": "i"} }}}, {"$group": {"_id": { "ecNumber": "$ecNumber", "sequences": "$firstAccessionCode", "substrate": "$ligandStructureId"}, "total": {"$sum": 1}}}, {"$project": {"ecNumber": "$_id.ecNumber", "sequence": "$_id.sequences", "substrate": "$_id.substrate", "total": "$total", "_id": 0}}, {"$sort": {"ecNumber": 1}}, {"$limit": 100000 } ]

miau_km = read_mongo(db, collection, pipeline2_km, host='localhost', port=27017, username=None, password=None, no_id=True)
miau_kcatkm = read_mongo(db, collection, pipeline2_kcatkm, host='localhost', port=27017, username=None, password=None, no_id=True)
miau_turnnum = read_mongo(db, collection, pipeline2_turnnum, host='localhost', port=27017, username=None, password=None, no_id=True)

#print(miau_km.head())
print(miau_km.shape)

for tag in ["km", "kcatkm", "turnnum"]:
	if tag == "km":
		tablefile=open("3.1.1*_%s.txt" % (tag), "wt")
		tablefile.write(tabulate(miau_km, tablefmt="fancy_grid"))
		tablefile.close()
	if tag == "kcatkm":
		tablefile=open("3.1.1*_%s.txt" % (tag), "wt")
		tablefile.write(tabulate(miau_kcatkm, tablefmt="fancy_grid"))
		tablefile.close()
	if tag == "turnnum":
		tablefile=open("3.1.1*_%s.txt" % (tag), "wt")
		tablefile.write(tabulate(miau_turnnum, tablefmt="fancy_grid"))
		tablefile.close()
		
		
#print(tabulate(miau_km, headers="firstrow", tablefmt="fancy_grid"))
#sns.heatmap(miau_km.total, cmap ='RdYlGn', linewidths = 0.30) #annot = True)

'''
#Bar graph for km
plt.bar(miau_km.miau, miau_km.total, width=0.1, bottom=None, align='center', color= "red")
plt.title("km")
plt.xlabel("Unique entries")
plt.ylabel("Number of km entries by number, sequence and substrate")
plt.xticks(rotation='vertical')
plt.show()'''


#####################################################################################################################

#Mencionar funciones de 

#gist.github.com/jmquintana79/eae522720ff571a6b496ddcd5cd69fe8







