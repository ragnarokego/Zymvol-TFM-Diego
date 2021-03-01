from zeep import Client
import hashlib
import os
import sys

#ABRIMOS NUESTRA CUENTA EN BRENDA
wsdl = "https://www.brenda-enzymes.org/soap/brenda_zeep.wsdl" #url que usa la API
email = "diego.ramirez@e-campus.uab.cat" #Mi e-mail de la cuenta de BRENDA
password = hashlib.sha256("Zymvol21".encode("utf-8")).hexdigest() #La contraseña está entre comillas

client = Client(wsdl)

parameters = (email,password)

def commonECnums(): 
	#Esta función pretende aplicarse a todas las listas, para finalmente tener una única lista con todos los EC numbers que tienen información para todos los parámetros que queremos:
	infofile=open("All_EC_Numbers.txt", "rt")
	outputfile=open("Common_EC_Numbers.txt","wt")
	ECNums_raw=infofile.readline()
	ECNums_str=ECNums_raw[1:(len(ECNums_raw)-1)]
	ECNums_list = ECNums_str.split(",")
	print(len(ECNums_list))
	while True: 	
		 	numbers_raw=infofile.readline()
		 	if not numbers_raw: break
		 	numbers_str=numbers_raw[1:(len(numbers_raw)-1)]
		 	list_numbers=numbers_str.split(",")
		 	for numero in ECNums_list:
		 		if numero not in list_numbers:
		 			ECNums_list.remove(numero)
	print(len(ECNums_list))
	
	for entrada in ECNums_list:
		outputfile.write(entrada)
		outputfile.write("\n")
	
	#Cerramos los archivos
	infofile.close()
	outputfile.close()

def allcommonECnums(parameters,client):
	#Primero, abrimos un fichero sobre el que vamos a escribir las listas con los números de cada parámetro
	commonECnumbers=open("All_EC_Numbers.txt", "wt")
	
	#Aquí están todos los EC numbers de las enzimas den la base de datos
	ECNums= client.service.getEcNumbersFromEcNumber(*parameters) 
	commonECnumbers.write(str(ECNums))
	commonECnumbers.write("\n")
	
	#A partir de aquí están los ECNumbers del resto de parámetros:
	#Aplicación
	ApplicNums = client.service.getEcNumbersFromApplication(*parameters) 
	commonECnumbers.write(str(ApplicNums))
	commonECnumbers.write("\n")
	#Nombre de las enzimas
	EnzynamesNums= client.service.getEcNumbersFromEnzymeNames(*parameters)
	commonECnumbers.write(str(EnzynamesNums))
	commonECnumbers.write("\n")
	#Valores de expresión
	ExpresNums = client.service.getEcNumbersFromExpression(*parameters)
	commonECnumbers.write(str(ExpresNums))
	commonECnumbers.write("\n")
	#Información general
	GeneralinfoNums = client.service.getEcNumbersFromGeneralInformation(*parameters)
	commonECnumbers.write(str(GeneralinfoNums))
	commonECnumbers.write("\n")
	#Estabilidad general
	GeneralstabNums = client.service.getEcNumbersFromGeneralStability(*parameters)
	commonECnumbers.write(str(GeneralstabNums))
	commonECnumbers.write("\n")
	#Valor IC50
	IC50Nums = client.service.getEcNumbersFromIc50Value(*parameters)
	commonECnumbers.write(str(IC50Nums))
	commonECnumbers.write("\n")
	# Inhibidores
	InhibNums = client.service.getEcNumbersFromInhibitors(*parameters)
	commonECnumbers.write(str(InhibNums))
	commonECnumbers.write("\n")
	# Constante cinética de inhibición
	KINums = client.service.getEcNumbersFromKiValue(*parameters)
	commonECnumbers.write(str(KINums))
	commonECnumbers.write("\n")
	# Constante cinética de Michaelis Menten
	KMNums = client.service.getEcNumbersFromKmValue(*parameters)
	commonECnumbers.write(str(KMNums))
	commonECnumbers.write("\n")
	# Ligandos
	LigandNums = client.service.getEcNumbersFromLigands(*parameters)
	commonECnumbers.write(str(LigandNums))
	commonECnumbers.write("\n")
	#Localización
	LocalizNums = client.service.getEcNumbersFromLocalization(*parameters)
	commonECnumbers.write(str(LocalizNums))
	commonECnumbers.write("\n")
	#Producto natural
	NaturprodNums = client.service.getEcNumbersFromNaturalProduct(*parameters)
	commonECnumbers.write(str(NaturprodNums))
	commonECnumbers.write("\n")
	#Sustrato natural
	NatursubsNums = client.service.getEcNumbersFromNaturalSubstrate(*parameters)
	commonECnumbers.write(str(NatursubsNums))
	commonECnumbers.write("\n")
	#Organismos en los que se encuentra
	OrganismNums = client.service.getEcNumbersFromOrganism(*parameters)
	commonECnumbers.write(str(OrganismNums))
	commonECnumbers.write("\n")
	#Referencia PDB
	PDBNums = client.service.getEcNumbersFromPdb(*parameters)
	commonECnumbers.write(str(PDBNums))
	commonECnumbers.write("\n")
	#pH óptimo
	PhoptNums = client.service.getEcNumbersFromPhOptimum(*parameters)
	commonECnumbers.write(str(PhoptNums))
	commonECnumbers.write("\n")
	#Rango pH
	PhrangeNums = client.service.getEcNumbersFromPhRange(*parameters)
	commonECnumbers.write(str(PhrangeNums))
	commonECnumbers.write("\n")
	#Estabilidad pH
	PhstabNums = client.service.getEcNumbersFromPhStability(*parameters)
	commonECnumbers.write(str(PhstabNums))
	commonECnumbers.write("\n")
	#Productos
	ProdNums = client.service.getEcNumbersFromProduct(*parameters)
	commonECnumbers.write(str(ProdNums))
	commonECnumbers.write("\n")
	#Purificación
	PurifNums = client.service.getEcNumbersFromPurification(*parameters)
	commonECnumbers.write(str(PurifNums))
	commonECnumbers.write("\n")
	#Reacciones
	ReacNums= client.service.getEcNumbersFromReaction(*parameters)
	commonECnumbers.write(str(PDBNums))
	commonECnumbers.write("\n")
	#Secuencias
	SeqNums = client.service.getEcNumbersFromSequence(*parameters)
	commonECnumbers.write(str(SeqNums))
	commonECnumbers.write("\n")
	#Specific activity
	SpecActNums = client.service.getEcNumbersFromSpecificActivity(*parameters)
	commonECnumbers.write(str(SpecActNums))
	commonECnumbers.write("\n")
	#Sustrato
	SubsNums = client.service.getEcNumbersFromSubstrate(*parameters)
	commonECnumbers.write(str(SubsNums))
	commonECnumbers.write("\n")
	#Temperatura óptima
	TempoptNums = client.service.getEcNumbersFromTemperatureOptimum(*parameters)
	commonECnumbers.write(str(TempoptNums))
	commonECnumbers.write("\n")
	#Rango de temperatura
	TemprangeNums = client.service.getEcNumbersFromTemperatureRange(*parameters)
	commonECnumbers.write(str(TemprangeNums))
	commonECnumbers.write("\n")
	#Estabilidad térmica
	TempstabNums = client.service.getEcNumbersFromTemperatureStability(*parameters)
	commonECnumbers.write(str(TempstabNums))
	commonECnumbers.write("\n")
	
	#cerramos el fichero con las listas
	commonECnumbers.close()

#Ahora, vamos a escribir un archivo de texto que tenga esos números:
allcommonECnums(parameters,client)
commonECnums()

