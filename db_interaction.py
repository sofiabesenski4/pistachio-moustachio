
"""
This module is meant to have everything to do with PostGreSQL database interaction, using the PyGreSQL wrapper

Contains 4 different query functions:
PHN_vs_DOB
PHN_vs_DOB_vs_partial_name
PHN_vs_partial_name
DOB_vs_partial_name




main():
Tested using a database stored on localhost called patient_db_test,
containing a patient named John Smitherzon w/ details:
Desired Patient's DOB : '2015', 2, '16'
Desired Patient's PHN : 9201406376


"""
import datetime
from pg import DB
"""
Simple initialize function for a pointer to a database
"""
def make_connection_to_db(database_name):	
	try:
		return DB(database_name)
	except:
		print("database named {} not found in system.".format(database_name))
		return

"""
This function is meant to enter a single patient/row into a table called public.patients, to a patients table stored within a specified database
Inputs: db_ptr: a pointer to a PyGreSQL database object. 
				Must contain the table: "public.patients" with the columns/attributes: {dob: datetime.date},{phn:str},{first_name:str},{last_name:str}
		new_patient_first_name: string object, specifiying the first name of the patient
		new_patient_last_naem: string object specifying the last name of the patient
		new_patient_phn: string object, unique and primary key for the rows in the table
		new_patient_dob_datetime_obj: datetime.date object, which represents the dob of the new patient
"""
def insert_patient_into_db(db_ptr, new_patient_first_name,new_patient_last_name,new_patient_dob_datetime_obj,new_patient_phn):
	
	try:
		assert "public.patients" in db_ptr.get_tables()
	except AssertionError:
		print("could not find public.patients db in patients_db_test on system")
		return
	try:
		assert "dob" and "phn" and "first_name" and "last_name" in db_ptr.get_attnames("public.patients")
	except AssertionError:
		print("could not find required column names: dob, phn, first_name, or last_name")
		return
	"""try:
		assert not db_ptr.get("public.patients", new_patient_phn)
	except:
		print("Patient with phn {} already exists in database".format(str(new_patient_phn)))
		return
	"""
	try:
		db_ptr.insert("public.patients",first_name=new_patient_first_name, last_name= new_patient_last_name,dob = new_patient_dob_datetime_obj,phn = new_patient_phn)
	except:
		print("phn {} already exists in database, cannot insert a duplicate".format(new_patient_phn))
	return
"""
Basically the above function, but for DB.inserttable, not DB.insert
"""
def insert_patient_tuples_into_db(db_ptr, patient_tuples):
	#tuples are of the form: (new_patient_phn,new_patient_first_name,new_patient_last_name,new_patient_dob_datetime_obj)
	try:
		assert "public.patients" in db_ptr.get_tables()
	except AssertionError:
		print("could not find public.patients db in patients_db_test on system")
		return
	try:
		assert  "phn" and "first_name" and "last_name" and "dob" in db_ptr.get_attnames("public.patients")
	except AssertionError:
		print("could not find required column names: dob, phn, first_name, or last_name")
		return
	db_ptr.inserttable("public.patients",patient_tuples)
	return

"""
FUNCTION: PHN_vs_DOB_vs_partial_name_query(db_ptr, found_PHNs, found_datetime_objs, found_names)
IDea: check the database to find a match of 
"""

def PHN_vs_DOB_vs_partial_name_query(db_ptr, found_PHNs, found_datetime_objs, found_full_names):
	if len(found_PHNs) == 0:
		return "missing one or more of the fields"
	if len(found_datetime_objs) == 0:
		return "missing one or more of the fields"
	if len(found_full_names) == 0:
		return "missing one or more of the fields"
	#these temp tables could have already been made, and if so, drop them and reinstantiate them 
	try:
		db_ptr.query("CREATE TABLE found_phns(phn text PRIMARY KEY, index integer UNIQUE);")
	except:
	#if they have been made already, delete them, then recreate them so we can make fresh and empty tables
		db_ptr.query("DROP TABLE found_phns;")
		db_ptr.query("CREATE TABLE  found_phns(phn text PRIMARY KEY, found_phn_index integer UNIQUE);")
		
	try:
		db_ptr.query("CREATE TABLE  found_dobs(dob date, found_date_index integer PRIMARY KEY);")
	except:
	#if they have been made already, delete them, then recreate them so we can make fresh and empty tables
		db_ptr.query("DROP TABLE found_dobs;")
		db_ptr.query("CREATE  TABLE found_dobs(dob date, found_date_index integer PRIMARY KEY);")
	try:
		db_ptr.query("CREATE TABLE  found_partial_names(partial_name text, partial_name_index integer PRIMARY KEY);")
	except:
	#if they have been made already, delete them, then recreate them so we can make fresh and empty tables
		db_ptr.query("DROP TABLE found_partial_names;")
		db_ptr.query("CREATE TABLE found_partial_names(partial_name text, partial_name_index integer PRIMARY KEY);")
	
#	print(db_ptr.get_tables())
	#each row must be in form of a tuple
	partial_name_list = []
	[[partial_name_list.append(part_name) for part_name in full_name.strip().split(" ")] for full_name in found_full_names]
	
	found_PHN_table = [tuple([x,phn_index]) for phn_index,x in enumerate(found_PHNs)]
	found_DOB_table = [tuple([found_datetime.isoformat(),found_date_index]) for found_date_index,found_datetime in enumerate(found_datetime_objs)]
	found_partial_name_table = [tuple([found_partial_name, index ]) for index,found_partial_name in enumerate(partial_name_list)]

#	print(found_PHN_table)
#	print(found_DOB_table)
	db_ptr.inserttable("public.found_phns", found_PHN_table)
	db_ptr.inserttable("public.found_dobs", found_DOB_table)
	db_ptr.inserttable("public.found_partial_names", found_partial_name_table)
	ret_val =  db_ptr.query("""select * from patients, found_phns, found_dobs, found_partial_names 
								where patients.phn=found_phns.phn and found_dobs.dob = patients.dob
								and (found_partial_names.partial_name = patients.first_name or found_partial_names.partial_name=patients.last_name);""") 
	#dropping the tables we made to crossreference DOB vs PHN in the public.patients table
	db_ptr.query("DROP TABLE found_phns;")
	db_ptr.query("DROP TABLE found_dobs;")
	db_ptr.query("DROP TABLE found_partial_names;")
	return ret_val
	
	
	
	
	
"""
Function: PHN_vs_DOB_query
Idea: meant to check a table called "public.patients" for any rows which contain a phn from a python list object, as well as an equal date in the form of a 
	  datetime.date object, with the intention of identifying the patient referenced in the medical letter by finding a match in both attributes.

Input:db_ptr: a PyGreSQL pointer to a db object on the local system
	  found_PHNs: a python list of 10 digit strings, representing all 10 digit numbers found in the medical letter pdf
	  found_DOBs_datetime_obj: a list of datetime.date objects, representing all the dates found in the medical letter pdf

Output: returns a string which represents rows from the public.patients table which contains both a PHN and DOB match from a SQL query
	   
"""
def PHN_vs_DOB_query(db_ptr, found_PHNs, found_datetime_objs):
	if len(found_PHNs) == 0:
		return "missing one or more of the fields"
	if len(found_datetime_objs) == 0:
		return "missing one or more of the fields"
	
	#these temp tables could have already been made, and if so, drop them and reinstantiate them 
	try:
		db_ptr.query("CREATE TABLE found_phns(phn text PRIMARY KEY, found_phn_index integer UNIQUE);")
	except:
	#if they have been made already, delete them, then recreate them so we can make fresh and empty tables
		db_ptr.query("DROP TABLE found_phns;")
		db_ptr.query("CREATE TABLE  found_phns(phn text PRIMARY KEY, found_phn_index integer UNIQUE);")
		
	try:
		db_ptr.query("CREATE TABLE  found_dobs(dob date, found_date_index integer PRIMARY KEY);")
	except:
	#if they have been made already, delete them, then recreate them so we can make fresh and empty tables
		db_ptr.query("DROP TABLE found_dobs;")
		db_ptr.query("CREATE  TABLE found_dobs(dob date, found_date_index integer PRIMARY KEY);")
	
#	print(db_ptr.get_tables())
	#each row must be in form of a tuple
	
	found_PHN_table = [tuple([x,phn_index]) for phn_index,x in enumerate(found_PHNs)]
	found_DOB_table = [tuple([x.isoformat(),found_date_index]) for found_date_index,x in enumerate(found_datetime_objs)]

#	print(found_PHN_table)
#	print(found_DOB_table)
	db_ptr.inserttable("public.found_phns", found_PHN_table)
	db_ptr.inserttable("public.found_dobs", found_DOB_table)
	ret_val =  db_ptr.query("""select * from patients, found_phns, found_dobs
									where patients.phn=found_phns.phn and found_dobs.dob = patients.dob;""") 
	#dropping the tables we made to crossreference DOB vs PHN in the public.patients table
	db_ptr.query("DROP TABLE found_phns;")
	db_ptr.query("DROP TABLE found_dobs;")
	
	return ret_val

"""
FUNCTION: PHN_vs_partial_name(db_ptr,found_PHNs,found_full_names)
IDEA: given the names and potential (10 digit) PHNs found in a pdf document, check to see if any of the patients in the patient database
		contains one of the found PHNs, as well as a first (inclusive)or last name match with the found names in the document. Both found_PHNs and 
		found_full_names
"""
def PHN_vs_partial_name_query(db_ptr, found_PHNs, found_full_names):
	if len(found_PHNs) == 0:
		return "missing one or more of the fields"
	if len(found_full_names) == 0:
		return "missing one or more of the fields"
	partial_name_list = []
	[[partial_name_list.append(part_name) for part_name in full_name.strip().split(" ")] for full_name in found_full_names]
	#print(partial_name_list)
	try:
		db_ptr.query("CREATE TABLE partial_names(part_name TEXT, part_name_index INTEGER PRIMARY KEY)")
	
	except:
		#the table exists
		db_ptr.query("DROP TABLE partial_names")
		db_ptr.query("CREATE TABLE partial_names(part_name TEXT, partial_name_index INTEGER PRIMARY KEY)")
	try:
		db_ptr.query("CREATE TABLE found_phns(found_phn text PRIMARY KEY, phn_index INTEGER UNIQUE)")
	except:
		db_ptr.query("DROP TABLE found_phns")
		db_ptr.query("CREATE TABLE found_phns(found_phn text PRIMARY KEY, phn_index INTEGER UNIQUE)")
	
	#the tables are made now
	
	found_PHN_table = [tuple([x,phn_index]) for phn_index,x in enumerate(found_PHNs)]
	found_partial_name_table = [tuple([found_partial_name, index ]) for index,found_partial_name in enumerate(partial_name_list)]
	db_ptr.inserttable("public.partial_names", found_partial_name_table)
	db_ptr.inserttable("public.found_phns", found_PHN_table)
	ret_val = db_ptr.query("""SELECT * from public.patients, public.partial_names, public.found_phns
								where (partial_names.part_name = patients.first_name or partial_names.part_name=patients.last_name)
									and (public.patients.phn = found_phns.found_phn); """)
	#print(db_ptr.query("SELECT * from partial_names"))
	#print(db_ptr.query("SELECT * from found_phns"))
	db_ptr.query("DROP table partial_names;")
	db_ptr.query("DROP table found_phns;")
	return ret_val
	
def DOB_vs_partial_name_query(db_ptr, found_datetime_objs, found_full_names):
	if len(found_datetime_objs) == 0:
		return "no matches"
	if len(found_full_names) == 0:
		return "no matches"
	#these temp tables could have already been made, and if so, drop them and reinstantiate them 	
	try:
		db_ptr.query("CREATE TABLE  found_dobs(dob date, found_date_index integer PRIMARY KEY);")
	except:
	#if they have been made already, delete them, then recreate them so we can make fresh and empty tables
		db_ptr.query("DROP TABLE found_dobs;")
		db_ptr.query("CREATE  TABLE found_dobs(dob date, found_date_index integer PRIMARY KEY);")
	try:
		db_ptr.query("CREATE TABLE  found_partial_names(partial_name text, partial_name_index integer PRIMARY KEY);")
	except:
	#if they have been made already, delete them, then recreate them so we can make fresh and empty tables
		db_ptr.query("DROP TABLE found_partial_names;")
		db_ptr.query("CREATE TABLE found_partial_names(partial_name text, partial_name_index integer PRIMARY KEY);")
	
#	print(db_ptr.get_tables())
	#each row must be in form of a tuple
	partial_name_list = []
	[[partial_name_list.append(part_name) for part_name in full_name.strip().split(" ")] for full_name in found_full_names]
	
	found_DOB_table = [tuple([found_datetime.isoformat(),found_date_index]) for found_date_index,found_datetime in enumerate(found_datetime_objs)]
	found_partial_name_table = [tuple([found_partial_name, index ]) for index,found_partial_name in enumerate(partial_name_list)]

#	print(found_PHN_table)
#	print(found_DOB_table)
	db_ptr.inserttable("public.found_dobs", found_DOB_table)
	db_ptr.inserttable("public.found_partial_names", found_partial_name_table)
	ret_val =  db_ptr.query("""select * from patients, found_dobs, found_partial_names 
								where found_dobs.dob = patients.dob
								and (found_partial_names.partial_name = patients.first_name or found_partial_names.partial_name=patients.last_name);""") 
	#dropping the tables we made to crossreference DOB vs partial name match in the public.patients table
	
	db_ptr.query("DROP TABLE found_dobs;")
	db_ptr.query("DROP TABLE found_partial_names;")
	return ret_val	
def PHN_query(db_ptr, found_PHNs):
	if len(found_PHNs) == 0:
		return "missing one or more of the fields"
	try:
		db_ptr.query("CREATE TABLE found_phns(found_phn text PRIMARY KEY, phn_index INTEGER UNIQUE)")
	except:
		db_ptr.query("DROP TABLE found_phns")
		db_ptr.query("CREATE TABLE found_phns(found_phn text PRIMARY KEY, phn_index INTEGER UNIQUE)")
	
	#the tables are made now
	
	found_PHN_table = [tuple([x,phn_index]) for phn_index,x in enumerate(found_PHNs)]
	db_ptr.inserttable("public.found_phns", found_PHN_table)
	ret_val = db_ptr.query("""SELECT * from public.patients, public.found_phns
								where (public.patients.phn = found_phns.found_phn); """)
	#print(db_ptr.query("SELECT * from partial_names"))
	#print(db_ptr.query("SELECT * from found_phns"))
	
	db_ptr.query("DROP table found_phns;")
	return ret_val

#the main class is used for testing, outside of super-program's environment
def main():
	print("main function call: testing module")
	db_name = "test_patients"
	db = make_connection_to_db(db_name)
	#print(db.query("Select* from patients;"))
	#insert_patient_into_db(db, "Thomas", "Besenski",  datetime.date(1994,10,4),"1234567891")
	#print(db.query("Select* from patients;"))
	
	#the following lists are supposed to mimic the found name/date/number lists given to us by the corenlp annotator
	person_list= ['Yakemchuk George Harvey', 'Yakemohuk George Harvey','Melvin', 'Rebecca Printed', 'Halzak Alison', 'Moisson Yvonne D', 'Tooby Debera', 'McDonald David Ian','John Smitherzon', 'Uttam Kavita', 'Hadwell Elizabeth', 'Yakemchuk George Harvey', 'Holness']

	date_list= ['Thursday', 'April 16 2015', 'Thursday April 16 2015', 'Friday', 'April 17 2015', 'Monday', 'February 16 2015', 'Thursday April 16 2015', 'Thursday April 16 2015', 'Thursday April 16 2015', 'Thursday April 16 2015', 'Thursday April 16 2015', 'Friday April 17 2015', 'Thursday April 16 2015']

	num_list= ['93379933','9201406376', '92014063765', '45-49 1','3751129774', '1', '45', '14', '2', '943379933', '73', '45-45', '50', '54',  '1-844-716-7743']

	found_date_list = [datetime.date(2015, 4, 16), datetime.date(2015, 4, 16), datetime.date(2015, 4, 17), datetime.date(2015, 2, 16), datetime.date(2015, 4, 16), datetime.date(2015, 4, 16), datetime.date(2015, 4, 16), datetime.date(2015, 4, 16), datetime.date(2015, 4, 16), datetime.date(2015, 4, 17), datetime.date(2015, 4, 16)]
#
	found_phn_list= ['9201406376', '844-716-7743']
	print("Querying PHN_vs_DOB\n",PHN_vs_DOB_query(db,found_phn_list,found_date_list))
	#gonna try to find the partial name match phn = 3751129774    first_name = Melvin
	print("Querying PHN_vs_partial_name\n", PHN_vs_partial_name_query(db,num_list,person_list))
	print("Querying PHN_vs_DOB_vs_partial_name\n", PHN_vs_DOB_vs_partial_name_query(db,num_list,found_date_list,person_list))
	print("Querying DOB_vs_partial_name\n", DOB_vs_partial_name_query(db,found_date_list,person_list))
if __name__ =="__main__":
	main()


