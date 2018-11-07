#deep_search.py
#This module contains the methods required for the pipeline to perform deeper search operations
"""
IDEA: 
Given either a datetime object representing a DOB or a string containing digits (PHN),
find all matches which correspond to one of either DOB or PHN


string_search(target,variance):
	patterns= 


generate_variance_patterns(target list):
	for index, char in enumerate(string):
		#print (str(index)+ " "+char)
		new_string = string[0:index] + "*" + string[index+1:]
		list_of_phn_string_patterns.append(new_string)
	return list_of_phn_string_patterns
	
"""




def generate_variance_patterns(target_list):
	return_patterns = []
	for target in target_list:
		for index, char in enumerate(target):
			#print (str(index)+ " "+char)
			new_string = string[0:index] + "*" + string[index+1:]
			list_of_patterns.append(new_string)
	return list_of_patterns
