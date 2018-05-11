"""
Created: Feb 9th 2018
Thomas Besenski

input parameters:$python3 main.py --d <DIRECTORY NAME CONTAINING PDFs>

This is the script which will iterate through each test file, processing it through tesseract ocr,
and then feeding the text into a java CoreNLPNER program to annotate the names of people in the medical letter,
and then calling the script to actually print the names to stdout 

there must be a stanford corenlp server running on the port 9000, and this will communicate
with that server, returning the output of the annotations.

The following command will start the server, from inside the corenlp folder:

java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -annotators "tokenize,ssplit,pos,lemma,parse,ner" -port 9000 -timeout 3000

PROGRAM FLOW:

updated Mar 3 2018
input-> directory containing the pdf documents

for all pdfs in directory:
	-convert pdf to jpg image using pdf2img module
	-enter jpg into pytesseract ocr engine to retrieve text
	
	-input text into StanfordCoreNLP Server running on port 9000, and annotate the text with Named Entity Recognition
	-filter through the annotations and store PERSON, DATE, and NUMBER elements
	
	-use precompiled regex to convert all the dates into a standardized format
	-use regex to determine which numbers could represent a PHN
	-store all the names, dates, and numbers in text files in the Test_Results folder
	-make a connection with a database on the local machine, containing the table "patients" with columns:
		PATIENT HEALTH NUMBER, FIRST_NAME, LAST_NAME, DATE OF BIRTH
	-find all matches of PHNs and DOBs found using NER, corresponding to patient entries in the database





"""
from shutil import copyfile
#using pytesseract as the ocr engine
import pytesseract
##using opencv to feed image input into tesseract
import cv2
import PIL
import os
#PIL is the python imaging library, used by opencv
from PIL import *
#PIL uses numpy to represent images
import numpy as np
from pdf2image import convert_from_path, convert_from_bytes
from stanfordcorenlp import StanfordCoreNLP
import db_interaction
import logging
import json
import sys
import re
import os
import argparse
import re
from enum import Enum
import datetime
#user defined modules
import Interact_with_Server as interact
import PDF_To_TXT as p2t

	
#initializing a dictionary to simplify recognizing the different date formats:
#DATE_MODES = {"DDMMYYYY":1,"MMDDYYYY":2,"YYYYMMDD":3}
def get_pdf_paths(directory_name):
	pdf_paths = []
	for pdf in os.listdir(directory_name):
		if pdf.endswith(".pdf"):
			pdf_paths.append(os.path.join(directory_name, pdf))	
	return pdf_paths
"""
strip_dates: to be used when given a list of potential dates
input: date_list= a list of found dates from the CoreNLP NER engine. can be in multiple different formats, and can contain extra numbers or characters
	   regex_pattern= a pre-compiled regex pattern which is used to filter out any "dates" retreived that aren't valid DOB candidates due to format, relative dating, etc..
	   valid_dates= a list of dates which have already been determined valid
	   DDMMYYYY = boolean value which determines the format of the regex pattern passed in, letting us know hot to  convert the found date into datetime format (ISO 8601)
	   YYYYMMDD = ^^ 
"""
def strip_dates(date_list, regex_pattern,valid_dates, DDMMYYYY, YYYYMMDD , MMDDYYYY):
	# pattern DDMMYYYY_date_strip should strip away any unnecessary numbers, before or after a date.
	#ie: "2 1995 May-10" could be annotated as a date if the OCR recognized "Page 2 1995 May-10" in the pdf
	#it accounts for dates which would be of the form DD MM YYYY or MM DD YYYY where the month can be 2 dig number or it can be the full month name
	# pattern YYYYMMDD_date_strip accounts for dates where the year appears first
	
	
	month_dict = {"January":1,"February":2,"March":3,"April":4,"May":5,"June":6,"July":7,"August":8,"September":9,"October":10,"November":11,"December":12,
				"Jan":1,"Feb":2,"Mar":3,"Apr":4,"May":5,"Jun":6,"Jul":7,"Aug":8,"Sep":9,"Oct":10,"Nov":11,"Dec":12,"1":1,
				"2":2,"3":3,"4":4,"5":5,"6":6,"7":7,"8":8,"9":9,"10":10,"11":11,"12":12,"01":1,
				"02":2,"03":3,"04":4,"05":5,"06":6,"07":7,"08":8,"09":9,"10":10,"11":11,"12":12}

	if DDMMYYYY:
		#print("DDMMYYYY")
		[valid_dates.append((re.search(regex_pattern, element).group(4),month_dict[re.search(regex_pattern, element).group(3)],re.search(regex_pattern, element).group(2))) for element in date_list if (re.search(regex_pattern, element) and re.search(regex_pattern, element).group(3) in month_dict)]
		#print(str(valid_dates))
	elif YYYYMMDD:
		#print("YYYYMMDD")
		[valid_dates.append((re.search(regex_pattern, element).group(2),month_dict[re.search(regex_pattern, element).group(3)],re.search(regex_pattern, element).group(4))) for element in date_list if (re.search(regex_pattern, element) and re.search(regex_pattern, element).group(3) in month_dict) ]
		#print(str(valid_dates))
	elif MMDDYYYY:
		#print("MMDDYYYY")
		[valid_dates.append((re.search(regex_pattern, element).group(4),month_dict[re.search(regex_pattern, element).group(2)],re.search(regex_pattern, element).group(3))) for element in date_list if (re.search(regex_pattern, element) and re.search(regex_pattern, element).group(2) in month_dict)]
		#print(str(valid_dates))
	return valid_dates
	
"""
find_dates: to be used on the entire text file extracted from the pdfs
"""
def find_dates(text, regex_pattern,valid_dates, DDMMYYYY, YYYYMMDD , MMDDYYYY):
	# pattern DDMMYYYY_date_strip should strip away any unnecessary numbers, before or after a date.
	#ie: "2 1995 May-10" could be annotated as a date if the OCR recognized "Page 2 1995 May-10" in the pdf
	#it accounts for dates which would be of the form DD MM YYYY or MM DD YYYY where the month can be 2 dig number or it can be the full month name
	# pattern YYYYMMDD_date_strip accounts for dates where the year appears first
	
	
	month_dict = {"January":1,"February":2,"March":3,"April":4,"May":5,"June":6,"July":7,"August":8,"September":9,"October":10,"November":11,"December":12,
				"Jan":1,"Feb":2,"Mar":3,"Apr":4,"May":5,"Jun":6,"Jul":7,"Aug":8,"Sep":9,"Oct":10,"Nov":11,"Dec":12,"1":1,
				"2":2,"3":3,"4":4,"5":5,"6":6,"7":7,"8":8,"9":9,"10":10,"11":11,"12":12,"01":1,
				"02":2,"03":3,"04":4,"05":5,"06":6,"07":7,"08":8,"09":9,"10":10,"11":11,"12":12}

	if DDMMYYYY:
		#print("DDMMYYYY")
		#print(regex_pattern.findall(text))
		[valid_dates.append((element[3],month_dict[element[2]],element[1])) for element in re.findall(regex_pattern,text, flags =re.IGNORECASE) if element[2] in month_dict]
		#print(str(valid_dates))
	elif YYYYMMDD:
		#print("YYYYMMDD")
		#print(regex_pattern.findall(text))
		[valid_dates.append((element[1],month_dict[element[2]],element[3])) for element in re.findall(regex_pattern,text, flags =re.IGNORECASE) if element[2] in month_dict]
		#print(str(valid_dates))
	elif MMDDYYYY:
		#print("MMDDYYYY")
		#print(regex_pattern.findall(text))
		[valid_dates.append((element[3],month_dict[element[1]],element[2])) for element in re.findall(regex_pattern,text, flags =re.IGNORECASE) if element[1] in month_dict]
		#print(str(valid_dates))
	
	return valid_dates

"""
Function:
Input: -list of identified numbers from the document
	   -regex pattern we are going to use to find a match
	   -list to mutate
	   
"""

def PHN_identifier(num_list, regex_pattern):
	"""

DDMMYYYY_date_pattern = r'((?:\d{1,2}|January|February|March|April|May|June|July|August|September|October|November|December)[\s\W]*(?:\d{1,2}|January|February|March|April|May|June|July|August|September|October|November|December)[\s\W]*\d{4})'
YYYYMMDD_date_pattern = r'(\d{4}[\s\W]*(?:\d{1,2}|January|February|March|April|May|June|July|August|September|October|November|December)[\s\W]*(?:\d{1,2}|January|February|March|April|May|June|July|August|September|October|November|December))'

	This pattern was tested on:
1234567891 =match
	1234-567891 =match
12345 67890 =match
123 23467 23 =match
1234567891 0 = 1234567891 match
1 1234567890 = 1234567890 match
	"""
	temp_list =[re.search(regex_pattern, element).group(0).replace(u"\xa0","") for element in num_list if re.search(regex_pattern, element)]
	temp_set = set(temp_list)
	temp_list = list(temp_set)
	return temp_list 
	#Notes on the regex pattern:
	#so we would prioritize finding an entire PHN with no spaces/etc in it, represented by the \d{10}
	#then we allow 10 occurences o	f a digit and any other delimiting character that is not a number or a new line
	#but also with a negative lookahead, so it will not match if there is a digit occuring after this second half of the or statement
	# prioritizing matches which have fewer delimiting characters
	
	"""
Function: patient_hypothesis(matches)	
INPUT:
	a tuple of lists of tuples: a tuple of A matches, B matches, C matches and D matches. Each X matches is a list of patient tuples, who matched in this category
														
	([(PHN,first_name,last_name,DOB),(),.....],[().....],[().....],[()......])
	
OUTPUT:
	a tuple: (Status, Match/None)
	status = "Multiple Matches of X" or ""
	 
	"""
def patient_hypothesis(matches):
	#if there is at least one match
	
	if matches[0] or matches[1] or matches[2] or matches[3]:
		if matches[0]:
			if len(matches)>1:
				return ("Multiple A Matches",str(list(set([(element[0],element[1],element[2],element[3]) for element in matches[0].getresult()]))))
			else:
				return ("A",str(matches[0][0]))
		elif matches[1]:
			if len(matches)>1:
				return ("Multiple B Matches",str(list(set([(element[0],element[1],element[2],element[3]) for element in matches[1].getresult()]))))
			else:
				return ("B",str(matches[1][0]))
		elif matches[2]:
			if len(matches)>1:
				return ("Multiple C Matches",str(list(set([(element[0],element[1],element[2],element[3]) for element in matches[2].getresult()]))))
			else:
				return ("C",str(matches[2][0]))
		else:
			if len(matches)>1:
				return ("Multiple D Matches",str(list(set([(element[0],element[1],element[2],element[3]) for element in matches[3].getresult()]))))
			else:
				return ("D",str(matches[3][0]))
		
	return (None)

"""
Function: create_list_from_annotations:
input: annotation_list: a list of tuples of form ("word/token","annotation keyword")
	   desired_annotation: a string which represents the annotatiion which we filter for to build an output list
output: a list of elements which were annotated with the "desired_annotation" tag. 
		Elements adjacent to each other, with the same "desired_annotation" tag, are concatenated together to form one list element.
		
		
"""
def main():
	ap = argparse.ArgumentParser()
	ap.add_argument("--f","--folder", required = True)
	ap.add_argument("--db","--database",required =True)
	args = ap.parse_args()

	
	
	#from stack overflow : https://stackoverflow.com/questions/3964681/find-all-files-in-a-directory-with-extension-txt-in-python
	#getting the names of all the files stored within that folder
	pdf_list = get_pdf_paths(str(args.f))
	database_name = args.db
	PHN_pattern = r'(\d{10})|((?:\d[^\n\d]?){10}(?!\d))'

	DDMMYYYY_date_pattern = r'((?<!\d\d)(\d{1,2})[^\na-zA-Z0-9]+(\d{1,2}|January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[^\na-zA-Z0-9]+(\d{4}))'
	YYYYMMDD_date_pattern = r'((\d{4})[^\n\w]+(\d{1,2}|January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[^\n\w]+(\d{1,2}))'
	MMDDYYYY_date_pattern = r'((\d{1,2}|January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[^\na-zA-Z0-9]+(\d{1,2})[^\na-zA-Z0-9]+(\d{4}))'
	compiled_DDMMYYYY_date_pattern = re.compile(DDMMYYYY_date_pattern)	
	compiled_YYYYMMDD_date_pattern = re.compile(YYYYMMDD_date_pattern)
	compiled_MMDDYYYY_date_pattern = re.compile(MMDDYYYY_date_pattern)
	compiled_PHN_pat = re.compile(PHN_pattern)
	corenlp_ptr = interact.init_corenlp()
	for index,pdf_path in enumerate(pdf_list):
		copyfile(pdf_path, "Test_Results/{}.pdf".format(index))
		fp = open("Test_Results/{}.txt".format(index), "w")
		text = p2t.convert_pdf_to_txt(pdf_path)
		
		#tuple: (PERSON[], DATE[], NUMBER[])
		per_day_num = interact.annotate_ner_with_corenlp(text.replace(",",""), corenlp_ptr)
		
		valid_dates = []
		#each of these strip_dates function calls appends each valid date match to the valid_dates list
		strip_dates(per_day_num[1],compiled_DDMMYYYY_date_pattern,valid_dates, DDMMYYYY=True, MMDDYYYY = False, YYYYMMDD = False )
		strip_dates(per_day_num[1],compiled_YYYYMMDD_date_pattern,valid_dates,DDMMYYYY= False, MMDDYYYY = False, YYYYMMDD = True)
		strip_dates(per_day_num[1],compiled_MMDDYYYY_date_pattern,valid_dates, DDMMYYYY= False,MMDDYYYY = True, YYYYMMDD = False)
		find_dates(text,compiled_DDMMYYYY_date_pattern,valid_dates, DDMMYYYY=True, MMDDYYYY = False, YYYYMMDD = False )
		find_dates(text,compiled_YYYYMMDD_date_pattern,valid_dates,DDMMYYYY= False, MMDDYYYY = False, YYYYMMDD = True)
		find_dates(text,compiled_MMDDYYYY_date_pattern,valid_dates, DDMMYYYY= False,MMDDYYYY = True, YYYYMMDD = False)
		found_datetimes = [datetime.date(int(date[0]),int(date[1]),int(date[2])) for date in valid_dates if 0<int(date[1])<13 and 0<int(date[2])<32 and 1900 < int(date[0])< 2018]
		
		#print("PERSON list :",str(per_day_num[0]))
		#print("CoreNLP's DATE list: ", str(per_day_num[1]))
		#print("NUMBER list: ", str(per_day_num[2]))
		#print("Regular expression's DATES list:", str(valid_dates))
		#print("Datetime.date objects: ", str(found_datetimes))
		#print("VALID PHN list: ", PHN_identifier(per_day_num[2],compiled_PHN_pat))
		#print("PATIENT HYPOTHESIS from highest frequency: " , patient_hypothesis(per_day_num[0]))
		fp.write("{}\nTest case #{} processed".format(str(pdf_path),index))
		
		fp.write("Person List: "+ str(per_day_num[0])+"\n\n")
		fp.write("CoreNLP's Date List: "+ str(per_day_num[1])+"\n\n")
		fp.write("Number list: "+ str(per_day_num[2])+"\n\n")
		fp.write("Verified Date List: "+ str(valid_dates)+"\n\n")
		fp.write("Valid PHN List: "+ str(PHN_identifier(per_day_num[2], compiled_PHN_pat))+"\n\n")
		db= db_interaction.make_connection_to_db(database_name)
		#print("Matches crossreferencing the DOB vs PHN:\n" , str(db_interaction.PHN_vs_DOB_query(db, PHN_identifier(per_day_num[2],compiled_PHN_pat), found_datetimes)))
		#print("\nMatches crossreferencing the PHN vs partial found names:\n" + str(db_interaction.PHN_vs_partial_name_query(db, PHN_identifier(per_day_num[2],compiled_PHN_pat), per_day_num[0])))
		#print("\nMatches crossreferencing the DOB vs partial found names:\n" + str(db_interaction.DOB_vs_partial_name_query(db, found_datetimes, per_day_num[0])))
		#print("\nMatches crossreferencing the PHN vs DOB vs partial found names\n" + str(db_interaction.PHN_vs_DOB_vs_partial_name_query(db, PHN_identifier(per_day_num[2],compiled_PHN_pat),found_datetimes,per_day_num[0])))
		PHN_vs_DOB_vs_partial_name_results =db_interaction.PHN_vs_DOB_vs_partial_name_query(db, PHN_identifier(per_day_num[2],compiled_PHN_pat),found_datetimes,per_day_num[0])
		PHN_vs_DOB_results = db_interaction.PHN_vs_DOB_query(db, PHN_identifier(per_day_num[2],compiled_PHN_pat), found_datetimes)
		PHN_vs_partial_name_results = db_interaction.PHN_vs_partial_name_query(db, PHN_identifier(per_day_num[2],compiled_PHN_pat), per_day_num[0])
		DOB_vs_partial_name_results = db_interaction.DOB_vs_partial_name_query(db, found_datetimes, per_day_num[0])
		
#This patient prediction is the variable which should be used to determine where the sample gets filed
		patient_prediction_result = patient_hypothesis((PHN_vs_DOB_vs_partial_name_results,PHN_vs_DOB_results,PHN_vs_partial_name_results,DOB_vs_partial_name_results))
		
"""
	Rest here is just to keep a log of the processed samples 
"""
		fp.write("\nPatient Hypothesis: " + str(patient_prediction_result))
		fp.write("\nA: Matches crossreferencing the PHN vs DOB vs partial found names\n" + str(PHN_vs_DOB_vs_partial_name_results))
		fp.write("\nB: Matches crossreferencing the PHN vs DOB:\n" + str(PHN_vs_DOB_results))
		fp.write("\nC: Matches crossreferencing the PHN vs partial found names:\n" + str(PHN_vs_partial_name_results))
		fp.write("\nD: Matches crossreferencing the DOB vs partial found names:\n" + str(PHN_vs_DOB_results))
		#fp.write("\nE: Matches referencing only the PHN\n" + str(PHN_query(db,PHN_identifier(per_day_num[2],compiled_PHN_pat))))
		fp.close()
if __name__ == "__main__":
	main()
