from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

#FUNCTION TO OPEN NEW DIRECTORIES 
def make_directory (name):
	if os.path.exists("./{}".format(name)):
		os.system("rm -rf ./{}".format(name))
	os.mkdir("./{}".format(name))
	
#FUNCTION TO EXTRACT THE INCHIKEYS
def extract_inchikeys(ligfile,trackfile,inchikeys,driver,id_list):
	#Read the ligand file
	while True:
		#The information is in a line recognized by a tag
		line = ligfile.readline().replace("\n","")
		if not line: break
		linenotab=line.replace(" ","")
		list_line = linenotab.split(":")
		
		#When we get to The tag of ligand Structure ID of BRENDA:
		if list_line[0] == "'ligandStructureId'":
			#We obtain the number
			number=list_line[1]
			
			#We check the number has not been already extracted
			if number not in id_list:
				id_list.append(number)
			elif number in id_list:
				continue
		
			#We open the page we want to crawl in
			driver.get("https://www.brenda-enzymes.org/ligand.php?brenda_ligand_id=%s" % (number))
	
			try:
				#We wait for the webpage to be fully ready
				WebDriverWait(driver, 180).until(EC.invisibility_of_element_located((By.ID, "myDiv")))
			
			except Exception:
				pass

			try:
				#We look of the first table with class "equal"
				search=driver.find_element_by_xpath('//div[@class="equal"]')
				
				#Counter of the rows
				numrow=0
				
				#We iterate through all the rows found in the table
				for row in search.find_elements_by_xpath('.//div[@class="row"]'):
					numrow+=1
					
					#The inchikey is in the second row, and will be always the last element
					if numrow==2:
						content=str(row.text)
						list_content=content.split(" ")	
						key = list_content[len(list_content)-1]
						inchikeys.write("%s %s\n" % (number, key))
				
				#We introduce a pause in order not to collapse the web spider
				#time.sleep(10)
				
				trackfile.write(number+" ")
				
			except Exception:
				inchikeys.write("%s None\n" % (number))		
				pass

#FUNCTION TO DO A NORMAL EXTRACTION
def normal_extraction(start, trackfile,id_list):
		
	#We open de Firefox web browser
	driver = webdriver.Firefox()
	
	for numfile in range(start, 16):
		#We open the file that contains the ligands ids
		ligfile = open("Property_Info/lig/Output_lig_%d.txt" %(numfile), "rt")

		#We create the file that relates the ligand id with its inchikey
		inchikeys = open("InChIKeys/InChIKeys_%d.txt" %(numfile), "wt")
		
		#We extract the InChIKeys
		extract_inchikeys(ligfile,trackfile,inchikeys,driver,id_list)
		
		#End print
		print ("File Output_lig_%d.txt ended." % (numfile))
		
		#Indicate End in trackfile
		trackfile.write("End\n")
		
		#Close opened files
		ligfile.close()
		inchikeys.close()
		trackfile.close()
		
	#We close the web browser				
	driver.close()

#FUNCTION TO DO A NORMAL EXTRACTION
def byec_extraction(trackfile,id_list):
		
	#We open de Firefox web browser
	driver = webdriver.Firefox()
	
	for line in open("Common_EC_Numbers.txt", "rt"):
		ecnumber=line[2:-2]
		print(ecnumber)
		
		#We open the file that contains the ligands ids
		ligfile = open("Property_Info2/lig/%s.txt" %(ecnumber), "rt")

		#We create the file that relates the ligand id with its inchikey
		inchikeys = open("InChIKeys/InChIKeys_%s.txt" %(ecnumber), "wt")
		
		#We extract the InChIKeys
		extract_inchikeys(ligfile,trackfile,inchikeys,driver,id_list)
		
		#End print
		print ("File %s.txt ended." % (ecnumber))
		
		#Indicate End in trackfile
		trackfile.write("End\n")
		
		#Close opened files
		ligfile.close()
		inchikeys.close()
		trackfile.close()
		
	#We close the web browser				
	driver.close()

#FUNCTION TO CONTINUE THE LAST EXTRACTION
def continue_extraction():
	#Initial print
	print("Continuing extraction. Going to where we left...")
	
	#We track the number of othe Output file in lig and the InChIKeys file
	numfile = 1 
	
	#We track the ligands ids extracted, in order not to repeat their extraction
	id_list=[]
	
	#We recover the last file and the id_list
	recoverfile = open("InChIKeys/Tracking_file.txt", "rt")
	while True:	
		raw_list = recoverfile.readline().replace("\n","").split(" ")
		print("El último elemento es: ", raw_list[len(raw_list)-1])
		print("Longitud de la lista: ", len(id_list))
		if raw_list[len(raw_list)-1] == "End":
			numfile += 1
			raw_list.pop()
			id_list.extend(raw_list)
			continue
		else:
			id_list.extend(raw_list)
			recoverfile.close()
			break
	
	#We open the file that contains the ligands ids
	ligfile = open("Property_Info/lig/Output_lig_%d.txt" %(numfile), "rt")

	#We reopen the file that relates the ligand id with its inchikey
	inchikeys = open("InChIKeys/InChIKeys_%d.txt" %(numfile), "a")
	
	#We reopen the file to store the track
	trackfile = open("InChIKeys/Tracking_file.txt", "a")
	
	#We open de Firefox web browser
	driver = webdriver.Firefox()
	
	#We extract the InChIKeys
	extract_inchikeys(ligfile,trackfile,inchikeys,driver,id_list)
	
	#End print
	print ("File Output_lig_%d.txt ended." % (numfile))
		
	#Indicate End in trackfile
	trackfile.write("End\n")
		
	#Close opened files
	ligfile.close()
	inchikeys.close()
	
	#We close the web browser				
	driver.close()
	
	#We continue the extraction normally
	normal_extraction(numfile+1, trackfile,id_list)
	
	#When we end, we close the trackfile
	trackfile.close()	

####################################################################################3

######## PROGRAM ###############

continuation=str(input("Do you want to continue last extraction? (y/n) "))

if continuation != "y":
	new=str(input("Do you want to start a new extraction? (y/n) "))
	if new != "y":
		quit()
	else:
		#Doing a new extraction
		print("Starting new extraction.")
		
		#First, we make the directory for our inchikeys
		make_directory("InChIKeys")
		
		#We create the file to store the track
		trackfile = open("InChIKeys/Tracking_file.txt", "wt")
		
		#We extract the data
		byec_extraction(trackfile, [])
		

else:
	#We continue the last extraction
	continue_extraction()
	
print("Extraction successful. Thanks for using this program.")





	


	
