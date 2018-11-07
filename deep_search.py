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
"""
code in bottoms-up.py
list_of_phn_string_patterns = []

#BUILDING THE PHN REGEX PATTERNS TO ALLOW ONE CHARACTER OF VARIANCE
for index, char in enumerate(string):
	#print (str(index)+ " "+char)
	new_string = string[0:index] + "*" + string[index+1:]
	list_of_phn_string_patterns.append(new_string)

connection_ptr = psycopg2.connect("dbname=test_patients user=thomas")
table_name = 'fax_test_1'

#QUERYING DATABASE FOR THE PHN FOUND
with connection_ptr.cursor() as curs:
	curs.execute("Select * from {} where {}.phn='{}';".format(table_name,table_name,string))
	ret = curs.fetchone()
	print(ret)
	
#NOW WE HAVE THE FIRST AND LAST NAME OF POTENTIAL PATIENT MATCHES
f = ret[1]
l = ret[2]
print("%r"%list_of_phn_string_patterns[0])


print(str(re.search(re.compile(list_of_phn_string_patterns[0]),text)))
"""



def generate_variance_patterns(target_list):
	return_patterns = []
	for target in target_list:
		for index, char in enumerate(target):
			#print (str(index)+ " "+char)
			new_string = string[0:index] + "*" + string[index+1:]
			list_of_patterns.append(new_string)
	return list_of_patterns
