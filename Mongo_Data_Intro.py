from mongoengine import *
import json
import re
import multiprocessing


#####################################################################################################################################

#We are going to define the CLASSES for each parameter. The name of each class will define a collection

class enzyme(Document): # ENZYME - EC NUMBER
	goNumber = StringField()
	ecNumber = StringField(primary_key=True)#the id of the document
	recommendedName = StringField()
	
	meta = {"allow_inheritance": True, 'collection':'enzyme'} #How to allow it to be used for a reference field
	
class literature(Document): #References
	reference = IntField(primary_key=True) #the id of the document
	title = StringField()
	journal = StringField()
	year = StringField()
	pubmedId = StringField()
	textmining = StringField()
	volume = StringField()
	authors = StringField()
	commentary = StringField()
	organism = StringField()
	pages = StringField()
	ecNumber = ReferenceField('enzyme', reverse_delete_rule=CASCADE) #If the user dissapears, this info dissapears too
	
	meta = {'allow_inheritance': True, 'collection':'literature' } #How to allow it to be used for a reference field

class ligand(Document): #Ligands
	organism = StringField()
	role = StringField()
	ligand = StringField()
	ecNumber = ReferenceField('enzyme', reverse_delete_rule=CASCADE)
	ligandStructureId = IntField(primary_key=True)
	inchikey = StringField()
	
	meta = {'allow_inheritance': True, 'collection':'ligand'} #How to allow it to be used for a reference field
	
class synonyms(Document): #Synonyms
	ecNumber = ReferenceField('enzyme', reverse_delete_rule=CASCADE)
	synonyms = StringField() 
	
	meta = {"allow_inheritance": True, 'collection': 'enzyme'} 
	
class reaction(Document): #Reaction
	reaction = StringField()
	commentary = StringField()
	literature = ReferenceField('literature')
	organism = StringField()
	ecNumber = ReferenceField('enzyme', reverse_delete_rule=CASCADE) #If the user dissapears, this info dissapears too
	
	meta = {"allow_inheritance": True, 'collection': 'enzyme'}

class reactype(Document): #Reaction Type
	reactionType = StringField()
	ecNumber = ReferenceField('enzyme', reverse_delete_rule=CASCADE)
	
	meta = {"allow_inheritance": True, 'collection': 'enzyme'}
	
class actcomp(Document):	#Activating Compound
	ecNumber= ReferenceField('enzyme', reverse_delete_rule=CASCADE)
	activatingCompound = StringField()
	organism= StringField()
	literature = ReferenceField('literature')
	commentary = StringField()
	
	meta = {"allow_inheritance": True, 'collection': 'enzyme'}

class app(Document): #Application
	ecNumber= ReferenceField('enzyme', reverse_delete_rule=CASCADE)
	organism = StringField()
	literature = ReferenceField('literature')
	commentary = StringField()
	application = StringField()
	
	meta = {"allow_inheritance": True, 'collection': 'enzyme'}
	
class cofact(Document): #Cofactor
	ecNumber = ReferenceField('enzyme', reverse_delete_rule=CASCADE)
	organism = StringField()
	literature = ReferenceField('literature')
	commentary = StringField()
	cofactor = StringField()
	ligandStructureId = ReferenceField('ligand')
	
	meta = {"allow_inheritance": True, 'collection': 'enzyme'}
	
class clon(Document): #Cloned
	ecNumber = ReferenceField('enzyme', reverse_delete_rule=CASCADE)
	organism = StringField()
	literature = ReferenceField('literature')
	commentary = StringField()
	
	meta = {"allow_inheritance": True, 'collection': 'enzyme'}

class dis(Document): #Disease
	ecNumber = ReferenceField('enzyme', reverse_delete_rule=CASCADE)
	titlePub = StringField()
	disease = StringField()
	pubmedId = StringField()
	
	meta = {"allow_inheritance": True, 'collection': 'enzyme'}
	
class expr(Document): #Expression information
	ecNumber = ReferenceField('enzyme', reverse_delete_rule=CASCADE)
	organism = StringField()
	literature = ReferenceField('literature')
	commentary = StringField()
	expression = StringField()
	
	meta = {"allow_inheritance": True, 'collection': 'enzyme'}
	
class geninfo(Document): #General Information
	ecNumber = ReferenceField('enzyme', reverse_delete_rule=CASCADE)
	organism = StringField()
	literature = ReferenceField('literature')
	commentary = StringField()
	generalInformation = StringField()
	
	meta = {"allow_inheritance": True, 'collection': 'enzyme'}

class genstab(Document): #General Stability
	ecNumber = ReferenceField('enzyme', reverse_delete_rule=CASCADE)
	organism = StringField()
	literature = ReferenceField('literature')
	generalStability = StringField()
	
	meta = {"allow_inheritance": True, 'collection': 'enzyme'}

class ic50(Document): #IC50 Value
	ecNumber = ReferenceField('enzyme', reverse_delete_rule=CASCADE)
	organism = StringField()
	literature = ReferenceField('literature')
	commentary = StringField()
	inhibitor = StringField()
	ic50Value = FloatField()
	ic50ValueMaximum = FloatField()
	ligandStructureId = ReferenceField('ligand')
	pH = FloatField()
	temperature = FloatField()
	
	meta = {"allow_inheritance": True, 'collection': 'enzyme'}

class inhib(Document): #Inhibitors
	ecNumber = ReferenceField('enzyme', reverse_delete_rule=CASCADE)
	organism = StringField()
	literature = ReferenceField('literature')
	commentary = StringField()
	inhibitor = StringField()
	ligandStructureId = ReferenceField('ligand')
	
	meta = {"allow_inheritance": True, 'collection': 'enzyme'}
	
class kcatkm(Document): #Catalytic Efficiency Value
	ecNumber = ReferenceField('enzyme', reverse_delete_rule=CASCADE)
	organism = StringField()
	literature = ReferenceField('literature')
	commentary = StringField()
	pH = FloatField()
	temperature = FloatField()
	substrate = StringField()
	ligandStructureId = ReferenceField('ligand')
	kcatKmValue = FloatField()
	kcatKmValueMaximum = FloatField()
	firstAccessionCode = StringField()
	
	meta = {"allow_inheritance": True, 'collection': 'enzyme'}
	
class ki(Document): #Inhibition constant
	ecNumber = ReferenceField('enzyme', reverse_delete_rule=CASCADE)
	organism = StringField()
	literature = ReferenceField('literature')
	commentary = StringField()
	pH = FloatField()
	temperature = FloatField()
	inhibitor = StringField()
	ligandStructureId = ReferenceField('ligand')
	kiValue = FloatField()
	kiValueMaximum = FloatField()
	
	meta = {"allow_inheritance": True, 'collection': 'enzyme'}
	
class km(Document): #Michaelis Menten constant
	ecNumber = ReferenceField('enzyme', reverse_delete_rule=CASCADE)
	organism = StringField()
	literature = ReferenceField('literature')
	commentary = StringField()
	pH = FloatField()
	temperature = FloatField()
	substrate = StringField()
	ligandStructureId = ReferenceField('ligand')
	kmValue = FloatField()
	kmValueMaximum = FloatField()
	firstAccessionCode = StringField()
	
	meta = {"allow_inheritance": True, 'collection': 'enzyme'}

class loc(Document): #Localization
	ecNumber = ReferenceField('enzyme', reverse_delete_rule=CASCADE)
	organism = StringField()
	literature = ReferenceField('literature')
	commentary = StringField()
	localization = StringField()
	textmining = IntField()
	idGo = StringField()
	
	meta = {"allow_inheritance": True, 'collection': 'enzyme'}
	
class metal(Document): #Metal ions
	ecNumber = ReferenceField('enzyme', reverse_delete_rule=CASCADE)
	organism = StringField()
	literature = ReferenceField('literature')
	commentary = StringField()
	metalsIons = StringField()
	ligandStructureId = ReferenceField('ligand')
	
	meta = {"allow_inheritance": True, 'collection': 'enzyme'}

class mw(Document): #Molecular weight
	ecNumber = ReferenceField('enzyme', reverse_delete_rule=CASCADE)
	organism = StringField()
	literature = ReferenceField('literature')
	commentary = StringField()
	molecularWeight = FloatField()
	molecularWeightMaximum = StringField() 
	
	meta = {"allow_inheritance": True, 'collection': 'enzyme'}
	#SE PODRÍA INTENTAR SACAR EL NOMBRE DE LA TÉCNICA/S USADAS PARA CALCULAR SU MASA MOLECULAR
	
class natprod(Document): #Natural products
	ecNumber = ReferenceField('enzyme', reverse_delete_rule=CASCADE)
	organism = StringField()
	literature = ReferenceField('literature')
	commentary = StringField()
	naturalReactionPartners = StringField()
	naturalProduct = StringField()
	ligandStructureId = ReferenceField('ligand')
	
	meta = {"allow_inheritance": True, 'collection': 'enzyme'}
	
class natsubs(Document): #Natural substrates
	ecNumber = ReferenceField('enzyme', reverse_delete_rule=CASCADE)
	organism = StringField()
	literature = ReferenceField('literature')
	commentary = StringField()
	naturalReactionPartners = StringField()
	naturalSubstrate = StringField()
	ligandStructureId = ReferenceField('ligand')
	
	meta = {"allow_inheritance": True, 'collection': 'enzyme'}
	
class oxstab(Document): #Oxidation stability
	ecNumber = ReferenceField('enzyme', reverse_delete_rule=CASCADE)
	organism = StringField()
	literature = ReferenceField('literature')
	oxidationStability = StringField()
	
	meta = {"allow_inheritance": True, 'collection': 'enzyme'}
	
class orgsolv(Document): #Organic Solvent Stability
	ecNumber = ReferenceField('enzyme', reverse_delete_rule=CASCADE)
	organism = StringField()
	literature = ReferenceField('literature')
	organicSolvent = StringField()
	commentary = StringField()
	
	meta = {"allow_inheritance": True, 'collection': 'enzyme'}
	
class path(Document): #Pathways in which the enzyme is present
	ecNumber = ReferenceField('enzyme', reverse_delete_rule=CASCADE)
	pathway = StringField()
	literature = ReferenceField('literature')
	link = StringField()
	source_database = StringField()

	meta = {"allow_inheritance": True, 'collection': 'enzyme'}

class pdb(Document): #PDB reference
	ecNumber = ReferenceField('enzyme', reverse_delete_rule=CASCADE)
	organism = StringField()
	pdb = StringField()
	
	meta = {"allow_inheritance": True, 'collection': 'enzyme'}
	
class phoptim(Document): #pH - Optimum
	ecNumber = ReferenceField('enzyme', reverse_delete_rule=CASCADE)
	organism = StringField()
	literature = ReferenceField('literature')
	phOptimum = FloatField()
	phOptimumMaximum = FloatField()
	commentary = StringField()
	
	meta = {"allow_inheritance": True, 'collection': 'enzyme'}
	
class phrange(Document): #pH - Range
	ecNumber = ReferenceField('enzyme', reverse_delete_rule=CASCADE)
	organism = StringField()
	literature = ReferenceField('literature')
	phRange = FloatField()
	phRangeMaximum = FloatField()
	commentary = StringField()
	
	meta = {"allow_inheritance": True, 'collection': 'enzyme'}
	
class phstab(Document): #pH - Stability
	ecNumber = ReferenceField('enzyme', reverse_delete_rule=CASCADE)
	organism = StringField()
	literature = ReferenceField('literature')
	phStability = FloatField()
	phStabilityMaximum = FloatField()
	commentary = StringField()
	
	meta = {"allow_inheritance": True, 'collection': 'enzyme'}
	
class pi(Document): #Isoelectric Point
	ecNumber = ReferenceField('enzyme', reverse_delete_rule=CASCADE)
	organism = StringField()
	literature = ReferenceField('literature')
	commentary = StringField()
	piValue = FloatField()
	piValueMaximum = FloatField()
	
	meta = {"allow_inheritance": True, 'collection': 'enzyme'}
	
class posttrad(Document): #Post-translational modifications
	ecNumber = ReferenceField('enzyme', reverse_delete_rule=CASCADE)
	organism = StringField()
	literature = ReferenceField('literature')
	commentary = StringField()
	posttranslationalModification = StringField()
	
	meta = {"allow_inheritance": True, 'collection': 'enzyme'}

class prod(Document): # Products
	ecNumber = ReferenceField('enzyme', reverse_delete_rule=CASCADE)
	organism = StringField()
	literature = ReferenceField('literature')
	commentary = StringField()
	reactionPartners = StringField()
	product = StringField()
	ligandStructureId = ReferenceField('ligand')
	
	meta = {"allow_inheritance": True, 'collection': 'enzyme'}
	
class protvar(Document): #Protein Variants by Protein Engineering
	ecNumber = ReferenceField('enzyme', reverse_delete_rule=CASCADE)
	organism = StringField()
	literature = ReferenceField('literature')
	commentary = StringField()
	engineering = StringField()
	
	meta = {"allow_inheritance": True, 'collection': 'enzyme'}
	
class purif(Document): #Purification
	ecNumber = ReferenceField('enzyme', reverse_delete_rule=CASCADE)
	organism = StringField()
	literature = ReferenceField('literature')
	commentary = StringField()
	
	meta = {"allow_inheritance": True, 'collection': 'enzyme'}

class seq(Document): #Sequence
	ecNumber = ReferenceField('enzyme', reverse_delete_rule=CASCADE)
	organism = StringField()
	source = StringField()
	noOfAminoAcids = IntField()
	firstAccessionCode = StringField(primary_key=True) #Make it the id of the document
	sequence = StringField()
	seq_id = IntField()
	
	meta = {"allow_inheritance": True, 'collection': 'sequence'}

class sourtis(Document): #Source Tissue
	ecNumber = ReferenceField('enzyme', reverse_delete_rule=CASCADE)
	organism = StringField()
	literature = ReferenceField('literature')
	commentary = StringField()
	sourceTissue = StringField()
	textmining = IntField()
	
	meta = {"allow_inheritance": True, 'collection': 'enzyme'}
	
class specact(Document): #Specific Activity
	ecNumber = ReferenceField('enzyme', reverse_delete_rule=CASCADE)
	organism = StringField()
	literature = ReferenceField('literature')
	commentary = StringField()
	specificActivityMaximum = FloatField()
	specificActivity = FloatField()
	pH = FloatField()
	temperature = FloatField()
	
	meta = {"allow_inheritance": True, 'collection': 'enzyme'}

class storstab(Document): #Storage Stability
	ecNumber = ReferenceField('enzyme', reverse_delete_rule=CASCADE)
	organism = StringField()
	literature = ReferenceField('literature')
	storageStability = StringField()
	pH = FloatField()
	temperature = FloatField() #To be parsed from storageStability
	time = StringField() #To be parse from storageStability
	
	meta = {"allow_inheritance": True, 'collection': 'enzyme'}
		
class subs(Document): #Substrates and Products
	ecNumber = ReferenceField('enzyme', reverse_delete_rule=CASCADE)
	organism = StringField()
	literature = ReferenceField('literature')
	commentary = StringField()
	reactionPartners = StringField()
	substrate = StringField()
	ligandStructureId = ReferenceField('ligand')
	
	meta = {"allow_inheritance": True, 'collection': 'enzyme'}
	
class subun(Document): #Subunits
	ecNumber = ReferenceField('enzyme', reverse_delete_rule=CASCADE)
	organism = StringField()
	literature = ReferenceField('literature')
	commentary = StringField()
	subunits = StringField()
	
	meta = {"allow_inheritance": True, 'collection': 'enzyme'}
	
class tempoptim(Document): #Temperature - Optimum
	ecNumber = ReferenceField('enzyme', reverse_delete_rule=CASCADE)
	organism = StringField()
	literature = ReferenceField('literature')
	commentary = StringField()
	temperatureOptimum = FloatField()
	temperatureOptimumMaximum = FloatField()
	
	meta = {"allow_inheritance": True, 'collection': 'enzyme'}
	
class temprange(Document): #Temperature - Range
	ecNumber = ReferenceField('enzyme', reverse_delete_rule=CASCADE)
	organism = StringField()
	literature = ReferenceField('literature')
	commentary = StringField()
	temperatureRange = FloatField()
	temperatureRangeMaximum = FloatField()
	
	meta = {"allow_inheritance": True, 'collection': 'enzyme'}
	
class tempstab(Document): #Temperature - Stability
	ecNumber = ReferenceField('enzyme', reverse_delete_rule=CASCADE)
	organism = StringField()
	literature = ReferenceField('literature')
	commentary = StringField()
	temperatureStability = FloatField()
	temperatureStabilityMaximum = FloatField()
	pH = FloatField() #Coming from parsing the commentary
	time = FloatField() #Coming from parsing the commentary
	half_life = FloatField() #Coming form parsing the commentary
	
	meta = {"allow_inheritance": True, 'collection': 'enzyme'}

class turnnum(Document): #Turnover Number
	ecNumber = ReferenceField('enzyme', reverse_delete_rule=CASCADE)
	organism = StringField()
	literature = ReferenceField('literature')
	commentary = StringField()
	substrate = StringField()
	ligandStructureId = ReferenceField('ligand')
	turnoverNumber = FloatField()
	turnoverNumberMaximum = FloatField()
	firstAccessionCode = StringField()
	hill_coef = FloatField() #Coming from parsing commentary
	pH = FloatField() #Coming from parsing commentary
	temperature = FloatField() #Coming from parsing commentary
	
	meta = {"allow_inheritance": True, 'collection': 'enzyme'}
	
########################################################################################################################

### FUNCTIONS

def parse(content, counter):
	content1=content.replace("None", "null")
	content2=content1.replace("\',@\'","\",\"")
	content3=content2.replace("{\'","{\"")
	content4=content3.replace("\",@","\",")
	content5=content4.replace("\': \'","\": \"")
	content6=content5.replace("\",\'", "\",\"")
	content7=content6.replace("\'@","\" ")		
	content8=content7.replace("\': \"", "\": \"")
	content9=content8.replace("\': [", "\": [") 
	content10=content9.replace("@"," ") 
	content11=content10.replace("\': null, \'", "\": null, \"")
	content12=content11.replace("Id': ", "Id\": ")
	content13=content12.replace("\\","")
	content_prepare=content13.replace("], '", "], \"")
	#print(content_prepare)
	#print(counter)

	content_dict = json.loads(content_prepare)
	return content_dict

def intro_enzyme(content_dict):
	entry = enzyme(**content_dict)
	entry.save()

def intro_literature(content_dict):
	#Change the format of the id to a list
	content_dict["reference"]= int(content_dict["reference"])
	
	entry = literature(**content_dict)
	entry.save()

def intro_ligand(content_dict, id_list, inchi_list):
	#The information in ligand is redundant
	entries = []
	
	#We need to add the inchikey to the ligand
	#We look for the position in which the inchikey is found.
	for position in range(len(id_list)):
		
		if content_dict["ligandStructureId"] == id_list[position]: #If the id of the entry is the same as in the line add the inchikey to the dictionary
			if inchi_list[position] == "None":
				content_dict["inchikey"] = "null"
			
			else:
				content_dict["inchikey"] = inchi_list[position]
	
	#Introduce the document in the database
	entry = ligand(**content_dict)
	entry.save() 
		
def intro_synonyms(content_dict):
	entry = synonyms(**content_dict)
	entry.save()		

def intro_reaction(content_dict): #Reaction
	entry = reaction(**content_dict)
	entry.save()

def intro_reactype(content_dict): #Reaction Type
	#Eliminate unneccesary keys as they are all 0 or None
	for key in ["organism", "commentary", "literature"]:
		if key == None:
			continue
		else:
			content_dict.pop(key)
	
	#Introduce the document in the database
	entry = reactype(**content_dict)
	entry.save()

def intro_actcomp(content_dict):
	entry = actcomp(**content_dict)
	entry.save()

def intro_app(content_dict):
	entry = app(**content_dict)
	entry.save()

def intro_cofact(content_dict):
	entry = cofact(**content_dict)
	entry.save()

def intro_clon(content_dict):
	entry = clon(**content_dict)
	entry.save()

def intro_dis(content_dict):
	entry = dis(**content_dict)
	entry.save()

def intro_expr(content_dict):
	entry = expr(**content_dict)
	entry.save()

def intro_geninfo(content_dict):
	entry = geninfo(**content_dict)
	entry.save()

def intro_genstab(content_dict):
	entry = genstab(**content_dict)
	entry.save()

def intro_ic50(content_dict):
	#Change the string values of numbers to float
	content_dict["ic50Value"] = float(content_dict["ic50Value"])
	if content_dict["ic50ValueMaximum"] == None:
		content_dict["ic50ValueMaximum"] = 0
	else:
		content_dict["ic50ValueMaximum"] = float(content_dict["ic50ValueMaximum"])
	
	try:
		#We parse values from the commentary field, that might be useful for future queries
		#TEMPERATURE
		temperature_search = re.search(r'.* (.+?)&deg;C .*', content_dict["commentary"])
		if temperature_search:
			temperature = temperature_search.group(1)
			content_dict["temperature"] = float(temperature)
	
		#PH
		ph_search = re.search(r'.* pH ([0-9]+\.[0-9]*).*', content_dict["commentary"])
		if ph_search:
			ph = ph_search.group(1)
			content_dict["pH"] = float(ph)	
	
	except TypeError:
		pass
				
	#Introduce the document in the database
	entry = ic50(**content_dict)
	entry.save()
	
def intro_inhib(content_dict):
	entry = inhib(**content_dict)
	entry.save()

def intro_kcatkm(content_dict):
	#Change the string values of numbers to float
	content_dict["kcatKmValue"]=float(content_dict["kcatKmValue"])
	if content_dict["kcatKmValueMaximum"] == None:
		content_dict["kcatKmValueMaximum"] = 0
	else:
		content_dict["kcatKmValueMaximum"] = float(content_dict["kcatKmValueMaximum"])
	
	relate_accession_kcatkm(content_dict)
	
	try:
		#We parse values from the commentary field, that might be useful for future queries
		#TEMPERATURE
		temperature_search = re.search(r'.* (.+?)&deg;C .*', content_dict["commentary"])
		if temperature_search:
			temperature = temperature_search.group(1)
			content_dict["temperature"] = float(temperature)
	
		#pH
		ph_search = re.search(r'.* pH ([0-9]+\.[0-9]*).*', content_dict["commentary"])
		if ph_search:
			ph = ph_search.group(1)
			content_dict["pH"] = float(ph)
	
	except TypeError:
		pass
		
	#Introduce the document in the database
	entry = kcatkm(**content_dict)
	entry.save()

def intro_ki(content_dict):
	#Change the string values of numbers to float
	content_dict["kiValue"]=float(content_dict["kiValue"])
	
	if content_dict["kiValueMaximum"] == None:
		content_dict["kiValueMaximum"] = 0
	else:
		content_dict["kiValueMaximum"] = float(content_dict["kiValueMaximum"])
	
	try:
		#We parse values from the commentary field, that might be useful for future queries
		#TEMPERATURE
		temperature_search = re.search(r'.* (.+?)&deg;C .*', content_dict["commentary"])
		if temperature_search:
			temperature = temperature_search.group(1)
			content_dict["temperature"] = float(temperature)
	
		#PH
		ph_search = re.search(r'.* pH ([0-9]+\.[0-9]*).*', content_dict["commentary"])
		if ph_search:
			ph = ph_search.group(1)
			content_dict["pH"] = float(ph)
		
	except TypeError:
		pass
				
	#Introduce the document in the database
	entry = ki(**content_dict)
	entry.save()

def intro_km(content_dict):
	#Change the string values of numbers to float
	content_dict["kmValue"]=float(content_dict["kmValue"])

	if content_dict["kmValueMaximum"] == None:
		content_dict["kmValueMaximum"] = 0
	else:
		content_dict["kmValueMaximum"] = float(content_dict["kmValueMaximum"])
	
	relate_accession_km(content_dict)
	
	try:
		#We parse values from the commentary field, that might be useful for future queries
		#TEMPERATURE
		temperature_search = re.search(r'.* (.+?)&deg;C .*', content_dict["commentary"])
		if temperature_search:
			temperature = temperature_search.group(1)
			content_dict["temperature"] = float(temperature)
	
		#PH
		ph_search = re.search(r'.* pH ([0-9]+\.[0-9]*).*', content_dict["commentary"])
		if ph_search:
			ph = ph_search.group(1)
			content_dict["pH"] = float(ph)
	
	except TypeError:
		pass
	
	except ValueError:
		pass
	
	#Introduce the document in the database
	entry = km(**content_dict)
	entry.save()

def intro_loc(content_dict):
	#Change the string values of numbers to float
	content_dict["textmining"]=int(content_dict["textmining"])
	
	#Introduce the document in the database
	entry = loc(**content_dict)
	entry.save()

def intro_metal(content_dict):
	entry = metal(**content_dict)
	entry.save()

def intro_mw(content_dict):
	#Change the string values of numbers to float
	content_dict["molecularWeight"]=int(content_dict["molecularWeight"])
	
	#Introduce the document in the database
	entry = mw(**content_dict)
	entry.save()

def intro_natprod(content_dict):
	entry = natprod(**content_dict)
	entry.save()

def intro_natsubs(content_dict):
	entry = natsubs(**content_dict)
	entry.save()

def intro_oxstab(content_dict):
	entry = oxstab(**content_dict)
	entry.save()

def intro_orgsolv(content_dict):
	entry = orgsolv(**content_dict)
	entry.save()
	
def intro_path(content_dict):
	entry = path(**content_dict)
	entry.save()

def intro_pdb(content_dict):
	entry = pdb(**content_dict)
	entry.save()
	
def intro_phoptim(content_dict):
	#Change the string values of numbers to float
	content_dict["phOptimum"]=float(content_dict["phOptimum"])
	if content_dict["phOptimumMaximum"] == None:
		content_dict["phOptimumMaximum"] = 0
	else:
		content_dict["phOptimumMaximum"] = float(content_dict["phOptimumMaximum"])
	
	#Introduce the document in the database
	entry = phoptim(**content_dict)
	entry.save()
	
def intro_phrange(content_dict):
	#Change the string values of numbers to float
	content_dict["phRange"]=float(content_dict["phRange"])
	if content_dict["phRangeMaximum"] == None:
		content_dict["phRangeMaximum"] = 0
	else:
		content_dict["phRangeMaximum"] = float(content_dict["phRangeMaximum"])
	
	#Introduce the document in the database
	entry = phrange(**content_dict)
	entry.save()

def intro_phstab(content_dict):
	#Change the string values of numbers to float
	content_dict["phStability"]=float(content_dict["phStability"])
	if content_dict["phStabilityMaximum"] == None:
		content_dict["phStabilityMaximum"] = 0
	else:
		content_dict["phStabilityMaximum"] = float(content_dict["phStabilityMaximum"])
	
	#Introduce the document in the database
	entry = phstab(**content_dict)
	entry.save()

def intro_pi(content_dict):
	#Change the string values of numbers to float
	content_dict["piValue"]=float(content_dict["piValue"])
	
	if content_dict["piValueMaximum"] == None:
		content_dict["piValueMaximum"] = 0
	else:
		content_dict["piValueMaximum"] = float(content_dict["piValueMaximum"])
	
	#Introduce the document in the database
	entry = pi(**content_dict)
	entry.save()

def intro_posttrad(content_dict):
	entry = posttrad(**content_dict)
	entry.save()

def intro_prod(content_dict):
	entry = prod(**content_dict)
	entry.save()

def intro_protvar(content_dict):
	entry = protvar(**content_dict)
	entry.save()

def intro_purif(content_dict):
	entry = purif(**content_dict)
	entry.save()

def intro_seq(content_dict):
	#Change the string values of numbers to int
	content_dict["noOfAminoAcids"]=int(content_dict["noOfAminoAcids"])
	content_dict["seq_id"]=content_dict.pop("id")
	
	#Introduce the document in the database
	entry = seq(**content_dict)
	entry.save()

def intro_sourtis(content_dict):
	#Change the string values of numbers to int
	content_dict["textmining"]=int(content_dict["textmining"])
	
	#Introduce the document in the database
	entry = sourtis(**content_dict)
	entry.save()
	
def intro_specact(content_dict):
	#Change the string values of numbers to float
	content_dict["specificActivity"]=float(content_dict["specificActivity"])
	
	if content_dict["specificActivityMaximum"] == None:
		content_dict["specificActivityMaximum"] = 0
	else:
		content_dict["specificActivityMaximum"] = float(content_dict["specificActivityMaximum"])
	
	#Introduce the document in the database
	entry = specact(**content_dict)
	entry.save()

def intro_storstab(content_dict):
	try:
		#We parse values from the storageStability field, that might be useful for future queries
		#TEMPERATURE
		temperature_search = re.search(r'.* (.+?)&deg;C .*', content_dict["storageStability"])
		if temperature_search:
			temperature = temperature_search.group(1)
			content_dict["temperature"] = float(temperature)
	
		#pH
		ph_search = re.search(r'.* pH ([0-9]+\.[0-9]*).*', content_dict["storageStability"])
		if ph_search:
			ph = ph_search.group(1)
			content_dict["pH"] = float(ph)
		
		#time
		time_search = re.search(r'.*( .{1,10} min| .{1,10} h| .{1,10} hour| .{1,10} day| .{1,10} week| .{1,10} month|.{1,10} year).*', content_dict["storageStability"])
		if time_search:
			time = time_search.group(1)
			content_dict["time"] = time
	
	except TypeError:
		pass
	
	except ValueError:
		pass
		
	#Introduce the document in the database
	entry = storstab(**content_dict)
	entry.save()

def intro_subs(content_dict):
	entry = subs(**content_dict)
	entry.save()

def intro_subun(content_dict):
	entry = subun(**content_dict)
	entry.save()

def intro_tempoptim(content_dict):
	#Change the string values of numbers to float
	content_dict["temperatureOptimum"]=float(content_dict["temperatureOptimum"])
	if content_dict["temperatureOptimumMaximum"] == None:
		content_dict["temperatureOptimumMaximum"] = 0
	else:
		content_dict["temperatureOptimumMaximum"] = float(content_dict["temperatureOptimumMaximum"])
	
	#Introduce the document in the database
	entry = tempoptim(**content_dict)
	entry.save()

def intro_temprange(content_dict):
	#Change the string values of numbers to float
	content_dict["temperatureRange"]=float(content_dict["temperatureRange"])
	if content_dict["temperatureRangeMaximum"] == None:
		content_dict["temperatureRangeMaximum"] = 0
	else:
		content_dict["temperatureRangeMaximum"] = float(content_dict["temperatureRangeMaximum"])
	
	#Introduce the document in the database
	entry = temprange(**content_dict)
	entry.save()

def intro_tempstab(content_dict):
	#Change the string values of numbers to float
	content_dict["temperatureStability"]=float(content_dict["temperatureStability"])
	if content_dict["temperatureStabilityMaximum"] == None:
		content_dict["temperatureStabilityMaximum"] = 0
	else:
		content_dict["temperatureStabilityMaximum"] = float(content_dict["temperatureStabilityMaximum"])
	
	try:
		#We parse values from the commentary field, that might be useful for future queries
		#pH
		ph_search = re.search(r'.* pH ([0-9]+\.[0-9]*).*', content_dict["commentary"])
		if ph_search:
			ph = ph_search.group(1)
			content_dict["pH"] = float(ph)
	
	except TypeError:
		pass
	
	except ValueError:
		pass
		
	#Introduce the document in the database
	entry = tempstab(**content_dict)
	entry.save()

def intro_turnnum(content_dict):
	#Change the string values of numbers to float
	content_dict["turnoverNumber"]=float(content_dict["turnoverNumber"])
	if content_dict["turnoverNumberMaximum"] == None:
		content_dict["turnoverNumberMaximum"] = 0
	else:
		content_dict["turnoverNumberMaximum"] = float(content_dict["turnoverNumberMaximum"])
	
	relate_accession_turnover(content_dict)
	
	try:
		#We parse values from the commentary field, that might be useful for future queries
		#TEMPERATURE
		temperature_search = re.search(r'.* (.+?)&deg;C .*', content_dict["commentary"])
		if temperature_search:
			temperature = temperature_search.group(1)
			content_dict["temperature"] = float(temperature)
	
		#pH
		ph_search = re.search(r'.* pH ([0-9]+\.[0-9]*).*', content_dict["commentary"])
		if ph_search:
			ph = ph_search.group(1)
			content_dict["pH"] = float(ph)
	
	except TypeError:
		pass
	
	except ValueError:
		pass
		
	#Introduce the document in the database
	entry = turnnum(**content_dict)
	entry.save()

#Selection function of the class of document to introduce
def select_intro(content_dict, tag): 
	if tag == 'actcomp': 
		intro_actcomp(content_dict)
	
	elif tag == "app":
		intro_app(content_dict)
	
	elif tag == "cofact":
		intro_cofact(content_dict)
	
	elif tag == "clon":
		intro_clon(content_dict)
	
	elif tag == "dis":
		intro_dis(content_dict)
	
	elif tag == "expr":
		intro_expr(content_dict)
	
	elif tag == "enzynames":
		intro_synonyms(content_dict)
	
	elif tag == "geninfo":
		intro_geninfo(content_dict)
	
	elif tag == "genstab":
		intro_genstab(content_dict)
	
	elif tag == "ic50":
		intro_ic50(content_dict)
	
	elif tag == "inhib":
		intro_inhib(content_dict)
	
	elif tag == "kcatkm":
		intro_kcatkm(content_dict)
	
	elif tag == "ki":
		intro_ki(content_dict)
	
	elif tag == "km":
		intro_km(content_dict)
	
	elif tag == "loc":
		intro_loc(content_dict)
	
	elif tag == "metal":
		intro_metal(content_dict)
	
	elif tag == "mw":
		intro_mw(content_dict)
	
	elif tag == "natprod":
		intro_natprod(content_dict)
	
	elif tag == "natsubs":
		intro_natsubs(content_dict)
	
	elif tag == "oxstab":
		intro_oxstab(content_dict)
	
	elif tag == "orgsolv":
		intro_orgsolv(content_dict)
	
	elif tag == "path":
		intro_path(content_dict)
	
	elif tag == "pdb":
		intro_pdb(content_dict)
		
	elif tag == "phoptim":
		intro_phoptim(content_dict)
	
	elif tag == "phrange":
		intro_phrange(content_dict)
	
	elif tag == "phstab":
		intro_phstab(content_dict)
	
	elif tag == "pi":
		intro_pi(content_dict)
	
	elif tag == "posttrad":
		intro_posttrad(content_dict)
	
	elif tag == "prod":
		intro_prod(content_dict)
	
	elif tag == "protvar":
		intro_protvar(content_dict)
	
	elif tag == "purif":
		intro_purif(content_dict)
	
	elif tag == "reac":
		intro_reaction(content_dict)
	
	elif tag == "reactype":
		intro_reactype(content_dict)
	
	elif tag == "recname":
		intro_enzyme(content_dict)
		
	elif tag == "ref":
		intro_literature(content_dict)
		
	elif tag == "seq":
		intro_seq(content_dict)
	
	elif tag == "sourtis":
		intro_sourtis(content_dict)
	
	elif tag == "specact":
		intro_specact(content_dict)
	
	elif tag == "storstab":
		intro_storstab(content_dict)
	
	elif tag == "subs":
		intro_subs(content_dict)
		
	elif tag == "subun":
		intro_subun(content_dict)
	
	elif tag == "tempoptim":
		intro_tempoptim(content_dict)
	
	elif tag == "temprange":
		intro_temprange(content_dict)
	
	elif tag == "tempstab":
		intro_tempstab(content_dict)
	
	elif tag == "turnnum":
		intro_turnnum(content_dict)

def introduce_data(list_tags): #Function to give the order to introduce the information for the specified properties in the list of tags. Not recommended for the whole ligand information. 
	#Opening of the output files with the information
	for tag in list_tags:
		for num in range(1,6):
			counter = 0
			for line in open("Property_Info/%s/Output_%s_%d.txt" % (tag, tag, num), "rt"):
				
				line=line.strip() #Read each line
				
				if line=="[]": #No information
					continue
				
				elif line =="[{": #Beginning of the documents for an EC number
					content="{"
				
				elif line =="}, {": #Separator of all the documents
					content+="}"
				
					content_dict = parse(content, counter) #From string to dictionary/document
					select_intro(content_dict, tag) #Introduce the document in the database
				
					content = "{"		
				
				elif line =="}]": #End of all the documents for an EC number
					content+="}"
				
					content_dict = parse(content, counter)
					select_intro(content_dict, tag)
					
				else:	#Inside the documents
					content+=line #Add info to the document
					content+="@" #Special separator to clean afterwards the string
	
				counter += 1
			print("Output_%s_%d.txt entries were introduced in the database." %(tag, num))
		print("Tag %s entries were introduced in the database." %(tag))

def introduce_ligands(lig_entries, start, stop): #Function to give the order to introduce the information for ligands.
	
	#initialize the list with ligand ids and inchikeys. Relation between them by position
	id_list=[]
	inchi_list=[]
	
	#We open the file that contains the inchikeys
	for line in open("InChIKeys/all_inchikeys.txt", "rt"):
		line=line.strip()
		list_content=line.split(" ") #Split the line in ID and inchikey
		id_list.append(int(list_content[0])) #Introduce the ligand id in the id_list
		inchi_list.append(list_content[1]) #Introduce the inchikey in the inchi_list
	
	#Opening of the output files with the information
	for num in range(start,stop):
		counter = 0 #Initialize line counter
		
		for line in open("Property_Info/lig/Output_lig_%d.txt" % (num), "rt"):
			
				line=line.strip() #Read each line
				
				if line=="[]": #No information
					continue
				elif line =="[{": #Beginning of the documents for an EC number
					content="{"
						
				elif line =="}, {": #Separator of all the documents
					content+="}"
				
					content_dict = parse(content, counter) #From string to dictionary/document
					
					#We eliminate redundant information keys
					for key in ["organism", "ecNumber"]:
						content_dict.pop(key)
						
					if content_dict not in lig_entries:
						lig_entries.append(content_dict) #Introduce the document in the list to avoid redundancy
						intro_ligand(content_dict, id_list, inchi_list ) #Introduce the document in the database
					elif content_dict in lig_entries:
						continue
				
					content = "{"		
				
				elif line =="}]": #End of all the documents for an EC number
					content+="}"
				
					content_dict = parse(content, counter)
					
					#We eliminate redundant information keys
					for key in ["organism", "ecNumber"]:
						content_dict.pop(key)
						
					if content_dict not in lig_entries:
						lig_entries.append(content_dict)
						intro_ligand(content_dict, id_list, inchi_list)
					elif content_dict in lig_entries:
						continue
						
				else:	#Inside the documents
					content+=line #Add info to the document
					content+="@" #Special separator to clean afterwards the string
				counter += 1 #Increase line
				
		print("Output_lig_%d.txt entries were introduced in the database." %(num))
	print("Tag lig entries were introduced in the database." )

def relate_accession_km(content_dict):
	
	#We introduce the sequence related to the experiment
	accessionfile = open("Protseq_Relation/%s.txt" % (content_dict["ecNumber"]) , "rt") #We open the file with the data that relates the kinetic info to the accession code of the sequence
	
	#We read the file
	for line in accessionfile:
		
		line = line.strip()
		info = line.split("/@/") #The accession code and its identifiers are separated by /@/
		
		#Commentary correction
		info[3] = info[3].replace(u"\N{DEGREE SIGN}"+"C", "&deg;C")
		if info[3] == "-":
			info[3] = None
		
		#Values correction	
		values = info[2].split(" - ")
		if len(values) > 1:
			info[2] = values[0]
		
		if info[2]=="" or info[2]=="additional information":
			info[2]="0"
		
		#Literature correction
		lits=info[1].split(",")
		if len(lits)>1:
			info[1]=lits[0]
			
		if content_dict["commentary"] == info[3] and content_dict["literature"][0] == int(info[1]) and content_dict["kmValue"] == float(info[2]): #The identifiers are recognized
			
			#We make sure that the number of sequences is just one
			check = info[0].split(",")
			
			if len(check) == 1:	
				content_dict["firstAccessionCode"] = info[0] #Introduce the accession code
				break
			
			elif len(check) > 1:
				content_dict["firstAccessionCode"] = "Multiple" #There are more than one accession code
				break
		
		elif content_dict["commentary"] != info[3] or content_dict["literature"][0] != int(info[1]) or str(content_dict["kmValue"]) != info[2]: #No identifiers recognized or not all means that there is no sequence associated
			content_dict["firstAccessionCode"] = None 

def relate_accession_kcatkm(content_dict):
	
	#We introduce the sequence related to the experiment
	accessionfile = open("Protseq_Relation/%s.txt" % (content_dict["ecNumber"]) , "rt") #We open the file with the data that relates the kinetic info to the accession code of the sequence
	
	#We read the file
	for line in accessionfile:
		
		line = line.strip()
		info = line.split("/@/") #The accession code and its identifiers are separated by /@/
		
		#Commentary correction
		info[3] = info[3].replace(u"\N{DEGREE SIGN}"+"C", "&deg;C")
		if info[3] == "-":
			info[3] = None
		
		#Values correction	
		values = info[2].split(" - ")
		if len(values) > 1:
			info[2] = values[0]
		
		if info[2]=="" or info[2]=="additional information":
			info[2]="0"
		
		#Literature correction
		lits=info[1].split(",")
		if len(lits)>1:
			info[1]=lits[0]
			
		if content_dict["commentary"] == info[3] and content_dict["literature"][0] == int(info[1]) and content_dict["kcatKmValue"] == float(info[2]): #The identifiers are recognized
			
			#We make sure that the number of sequences is just one
			check = info[0].split(",")
			
			if len(check) == 1:	
				content_dict["firstAccessionCode"] = info[0] #Introduce the accession code
				break
			
			elif len(check) > 1:
				content_dict["firstAccessionCode"] = "Multiple" #There are more than one accession code
				break
		
		elif content_dict["commentary"] != info[3] or content_dict["literature"][0] != int(info[1]) or str(content_dict["kcatKmValue"]) != info[2]: #No identifiers recognized or not all means that there is no sequence associated
			content_dict["firstAccessionCode"] = None 

def relate_accession_turnover(content_dict):
	
	#We introduce the sequence related to the experiment
	accessionfile = open("Protseq_Relation/%s.txt" % (content_dict["ecNumber"]) , "rt") #We open the file with the data that relates the kinetic info to the accession code of the sequence
	
	#We read the file
	for line in accessionfile:
		
		line = line.strip()
		info = line.split("/@/") #The accession code and its identifiers are separated by /@/
		
		#Commentary correction
		info[3] = info[3].replace(u"\N{DEGREE SIGN}"+"C", "&deg;C")
		if info[3] == "-":
			info[3] = None
		
		#Values correction	
		values = info[2].split(" - ")
		if len(values) > 1:
			info[2] = values[0]
		
		if info[2]=="" or info[2]=="additional information":
			info[2]="0"
		
		#Literature correction
		lits=info[1].split(",")
		if len(lits)>1:
			info[1]=lits[0]
			
		if content_dict["commentary"] == info[3] and content_dict["literature"][0] == int(info[1]) and content_dict["turnoverNumber"] == float(info[2]): #The identifiers are recognized
			
			#We make sure that the number of sequences is just one
			check = info[0].split(",")
			
			if len(check) == 1:	
				content_dict["firstAccessionCode"] = info[0] #Introduce the accession code
				break
			
			elif len(check) > 1:
				content_dict["firstAccessionCode"] = "Multiple" #There are more than one accession code
				break
		
		elif content_dict["commentary"] != info[3] or content_dict["literature"][0] != int(info[1]) or str(content_dict["turnoverNumber"]) != info[2]: #No identifiers recognized or not all means that there is no sequence associated
			content_dict["firstAccessionCode"] = None 

############################################################################################################

### PROGRAM

#The database will not be created until we add info to it. Because of that we will do it using Mongo Engine. 
connect('Zymvol_DRR_2021')

#PARSE OF THE OUTPUT FILES FROM SOAP CLIENT

#Introduction of the list with all the tags for each property
list_tags =['seq']

'''['actcomp','app','cas', 'clon', 'cofact', 'dis', 'enzynames', 'expr', 'geninfo', 'genstab', 'ic50', 'inhib',
	 'kcatkm', 'ki', 'km', 'loc', 'metal', 'mw', 'natprod', 'natsubs', 'orgsolv', 'orgn', 'oxstab', 'ref', 'path',
	 'pdb', 'phoptim', 'phrange', 'phstab', 'pi', 'posttrad', 'prod', 'protvar', 'purif', 'reac', 'reactype','recname', 
	 'seq', 'sourtis', 'specact', 'storstab', 'subs', 'subun', 'syn', 'tempoptim', 'temprange', 'tempstab', 
	 'turnnum']'''

#Introduce the information in the files with the tag directory name
introduce_data(list_tags)

#We introduce ligands apart because of the information redundance
lig_entries=[]

#introduce_ligands(lig_entries, 1, 16)

'''
id_list=[]
inchi_list=[]
#We open the file that contains the inchikeys
for line in open("InChIKeys/all_inchikeys.txt", "rt"):
	line=line.strip()
	list_content=line.split(" ") #Split the line in ID and inchikey
	id_list.append(int(list_content[0]))
	inchi_list.append(list_content[1])

	
	
	if content_dict["ligandStructureId"] == int(list_content[0]): #If the id of the entry is the same as in the line add the inchikey to the dictionary
		if list_content[1] == "None":
			content_dict["inchikey"] = "null"	
		else:
			content_dict["inchikey"] = list_content[1]
	

for num in range(1,16):
	counter = 0
	for line in open("Property_Info/lig/Output_lig_%d.txt" % (num), "rt"):
		
			line=line.strip()
			
			if line=="[]":
				continue
			elif line =="[{":
				content="{"
					
			elif line =="}, {":
				content+="}"
			
				content_dict = parse(content, counter)
				
				if content_dict not in lig_entries:
					lig_entries.append(content_dict)
					intro_ligand(content_dict, id_list, )
				elif content_dict in lig_entries:
					continue
			
				content = "{"		
			
			elif line =="}]":
				content+="}"
			
				content_dict = parse(content, counter)
				if content_dict not in lig_entries:
					lig_entries.append(content_dict)
					intro_ligand(content_dict)
				elif content_dict in lig_entries:
					continue
					
			else:	
				content+=line
				content+="@"

			counter += 1
			
	print("Output_lig_%d.txt entries were introduced in the database." %(num))
print("Tag lig entries were introduced in the database." )
'''

