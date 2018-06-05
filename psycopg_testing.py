#psycopg_testing.py
from psycopg2 import sql
import psycopg2
import datetime

#print(psycopg2.__version__)
#conn = psycopg2.connect("dbname = test_patients user=teb8")
#db_ptr = conn.cursor()
#results = db_ptr.execute("SELECT * FROM iclinic_data;")
#print("first: ",str(db_ptr.fetchone()))
#print("second: ", str(db_ptr.fetchone()))
#print("third: ", str(db_ptr.fetchone()))
#print(str(db_ptr.fetchall()))

#the following methods need to be satisfied:
#def insert_patient_tuples_into_db(db_ptr, patient_tuples):
"""
Input: database_name = name of postgresql database to connect to 
	   username = the username which we are attempting to connect to the postgresql database with 
Output:conn_ptr = connection pointer to the postgresql database. A transactional database cursor must be instantiated before anything
					can be done with the specific table, but by separating these pointers, each transaction will be recorded in a long
					session
"""

def make_connection_to_db(database_name,username):
	try:
		conn_ptr = psycopg2.connect("dbname={} user={}".format(database_name,username))
		return conn_ptr
	except:
		print("error encountered when trying to connect to the database{} with username{}".format(database_name,username))
		
	

"""
Input: conn_ptr = psycopg2 connection object to the database we are dealing with
	   patient_tuple = patient to be inserted into the database, taking the form (string PHN, string first_name, string last_name, datetime_object DOB)
"""
def insert_patient_into_db(conn_ptr,patient_tuple,table_name):
	#using a with statement here makes this happen in one postgresql transaction, which is recorded
	with conn_ptr:
		with conn_ptr.cursor() as db_ptr:
			print(str(patient_tuple))
			db_ptr.execute( sql.SQL("Insert into {} values (%s,%s,%s,%s)").format(sql.Identifier(table_name)) , patient_tuple)
			db_ptr.close()

def select_all(conn_ptr, table_name):
	with conn_ptr:
		with conn_ptr.cursor() as db_ptr:
			db_ptr.execute(sql.SQL("Select * from {};").format(sql.Identifier(table_name)))
			for record in db_ptr:
				print(record)
			db_ptr.close()
#def PHN_vs_DOB_vs_partial_name_query(db_ptr, found_PHNs, found_datetime_objs, found_full_names)
def PHN_vs_DOB_vs_partial_name_query(connection_ptr, found_PHNs, found_datetime_objs, found_full_names, table_name):
	if len(found_PHNs) == 0 or len(found_datetime_objs) == 0 or len(found_full_names)==0:
		return None
	with connection_ptr:
		with connection_ptr.cursor() as db_ptr:
			
			db_ptr.execute("""SELECT table_name FROM information_schema.tables
									WHERE table_schema = 'public'""")
			
			for table in db_ptr.fetchall():
				if "found_phns" in table:
					db_ptr.execute("drop table found_phns;")
				elif "found_dobs" in table:
					db_ptr.execute("drop table found_dobs;")
				elif "found_partial_names" in table:
					db_ptr.execute("drop table found_partial_names;")
			try:
				db_ptr.execute("CREATE TABLE found_phns(phn text PRIMARY KEY, index integer UNIQUE);")
			except:
				
				print("error occured when trying to create found_phns table in  PHN_vs_DOB_vs_partial_name_query")
				return
			try:
				db_ptr.execute("CREATE TABLE  found_dobs(dob date, found_date_index integer PRIMARY KEY);")
			except :
			#if they have been made already, delete them, then recreate them so we can make fresh and empty tables

				print("error occured when trying to create found_dob table in  PHN_vs_DOB_vs_partial_name_query")
				return
			try:
				db_ptr.execute("CREATE TABLE  found_partial_names(partial_name text, partial_name_index integer PRIMARY KEY);")
			except:
			#if they have been made already, delete them, then recreate them so we can make fresh and empty tables
				print("error occured when trying to create found_partial_names table in  PHN_vs_DOB_vs_partial_name_query")
				return
			partial_name_list = []
			[[partial_name_list.append(part_name) for part_name in full_name.strip().split(" ")] for full_name in found_full_names]
			
			found_PHN_list = [tuple([x,phn_index]) for phn_index,x in enumerate(found_PHNs)]
			found_DOB_list = [tuple([found_datetime.isoformat(),found_date_index]) for found_date_index,found_datetime in enumerate(found_datetime_objs)]
			found_partial_name_list = [tuple([found_partial_name, index ]) for index,found_partial_name in enumerate(partial_name_list)]
			
			[db_ptr.execute("Insert into found_phns values (%s,%s)", element) for element in found_PHN_list]
			
			[db_ptr.execute("Insert into found_dobs values (%s,%s)", element) for element in found_DOB_list]
			
			[db_ptr.execute("Insert into found_partial_names values (%s,%s)", element) for element in found_partial_name_list]
			
			db_ptr.execute("""select * from iclinic_data, found_phns, found_dobs, found_partial_names 
								where iclinic_data.phn=found_phns.phn and found_dobs.dob = iclinic_data.dob
								and (lower(found_partial_names.partial_name) = lower(iclinic_data.first_name) or lower(found_partial_names.partial_name)=lower(iclinic_data.last_name));""") 
			ret_list = db_ptr.fetchall()
			db_ptr.execute("DROP table found_phns;")
			db_ptr.execute("DROP table found_dobs;")
			db_ptr.execute("DROP table found_partial_names;")
			if len(ret_list) ==0:
				return None
			else:
				return ret_list
			
def PHN_vs_DOB_query(connection_ptr, found_PHNs, found_datetime_objs, table_name):
	if len(found_PHNs) == 0 or len(found_datetime_objs) ==0:
		return None
	with connection_ptr:
		with connection_ptr.cursor() as db_ptr:
			
			db_ptr.execute("""SELECT table_name FROM information_schema.tables
									WHERE table_schema = 'public'""")
			
			for table in db_ptr.fetchall():
				if "found_phns" in table:
					db_ptr.execute("drop table found_phns;")
				elif "found_dobs" in table:
					db_ptr.execute("drop table found_dobs;")
			try:
				db_ptr.execute("CREATE TABLE found_phns(phn text PRIMARY KEY, index integer UNIQUE);")
			except:
				
				print("error occured when trying to create found_phns table in  PHN_vs_DOB_vs_partial_name_query")
			try:
				db_ptr.execute("CREATE TABLE  found_dobs(dob date, found_date_index integer PRIMARY KEY);")
			except :
			#if they have been made already, delete them, then recreate them so we can make fresh and empty tables

				print("error occured when trying to create found_dob table in  PHN_vs_DOB_vs_partial_name_query")
			
			found_PHN_list = [tuple([x,phn_index]) for phn_index,x in enumerate(found_PHNs)]
			found_DOB_list = [tuple([found_datetime.isoformat(),found_date_index]) for found_date_index,found_datetime in enumerate(found_datetime_objs)]
			
			[db_ptr.execute("Insert into found_phns values (%s,%s)", element) for element in found_PHN_list]
			
			[db_ptr.execute("Insert into found_dobs values (%s,%s)", element) for element in found_DOB_list]
			
			
			db_ptr.execute("""select * from iclinic_data, found_phns, found_dobs 
								where iclinic_data.phn=found_phns.phn and found_dobs.dob = iclinic_data.dob;""") 
			ret_list = db_ptr.fetchall()
			db_ptr.execute("DROP table found_phns;")
			db_ptr.execute("DROP table found_dobs;")
			
			if len(ret_list) ==0:
				return None
			else:
				return ret_list
def PHN_vs_partial_name_query(connection_ptr, found_PHNs, found_full_names, table_name):
	if len(found_PHNs) == 0 or len(found_full_names)==0:
		return None
	with connection_ptr:
		with connection_ptr.cursor() as db_ptr:
			
			db_ptr.execute("""SELECT table_name FROM information_schema.tables
									WHERE table_schema = 'public'""")
			
			for table in db_ptr.fetchall():
				if "found_phns" in table:
					db_ptr.execute("drop table found_phns;")
				elif "found_partial_names" in table:
					db_ptr.execute("drop table found_partial_names;")
			try:
				db_ptr.execute("CREATE TABLE found_phns(phn text PRIMARY KEY, index integer UNIQUE);")
			except:
				
				print("error occured when trying to create found_phns table in  PHN_vs_DOB_vs_partial_name_query")
				return
			try:
				db_ptr.execute("CREATE TABLE  found_partial_names(partial_name text, partial_name_index integer PRIMARY KEY);")
			except:
			#if they have been made already, delete them, then recreate them so we can make fresh and empty tables
				print("error occured when trying to create found_partial_names table in  PHN_vs_DOB_vs_partial_name_query")
				return
			partial_name_list = []
			[[partial_name_list.append(part_name) for part_name in full_name.strip().split(" ")] for full_name in found_full_names]
			
			found_PHN_list = [tuple([x,phn_index]) for phn_index,x in enumerate(found_PHNs)]
			found_partial_name_list = [tuple([found_partial_name, index ]) for index,found_partial_name in enumerate(partial_name_list)]
			
			[db_ptr.execute("Insert into found_phns values (%s,%s)", element) for element in found_PHN_list]
			
			
			[db_ptr.execute("Insert into found_partial_names values (%s,%s)", element) for element in found_partial_name_list]
			
			db_ptr.execute("""select * from iclinic_data, found_phns, found_partial_names 
								where iclinic_data.phn=found_phns.phn and
								 (lower(found_partial_names.partial_name) = lower(iclinic_data.first_name) or lower(found_partial_names.partial_name)=lower(iclinic_data.last_name));""") 
			ret_list = db_ptr.fetchall()
			db_ptr.execute("DROP table found_phns;")
			
			db_ptr.execute("DROP table found_partial_names;")
			if len(ret_list) ==0:
				return None
			else:
				return ret_list
def DOB_vs_partial_name_query(connection_ptr, found_datetime_objs, found_full_names, table_name):
	if len(found_datetime_objs) == 0 or len(found_full_names)==0:
		return None
	with connection_ptr:
		with connection_ptr.cursor() as db_ptr:
			
			db_ptr.execute("""SELECT table_name FROM information_schema.tables
									WHERE table_schema = 'public'""")
			
			for table in db_ptr.fetchall():
				if "found_dobs" in table:
					db_ptr.execute("drop table found_dobs;")
				elif "found_partial_names" in table:
					db_ptr.execute("drop table found_partial_names;")
			try:
				db_ptr.execute("CREATE TABLE  found_dobs(dob date, found_date_index integer PRIMARY KEY);")
			except :
			#if they have been made already, delete them, then recreate them so we can make fresh and empty tables

				print("error occured when trying to create found_dob table in  PHN_vs_DOB_vs_partial_name_query")
				return
			try:
				db_ptr.execute("CREATE TABLE  found_partial_names(partial_name text, partial_name_index integer PRIMARY KEY);")
			except:
			#if they have been made already, delete them, then recreate them so we can make fresh and empty tables
				print("error occured when trying to create found_partial_names table in  PHN_vs_DOB_vs_partial_name_query")
				return
			partial_name_list = []
			[[partial_name_list.append(part_name) for part_name in full_name.strip().split(" ")] for full_name in found_full_names]
			
			found_DOB_list = [tuple([found_datetime.isoformat(),found_date_index]) for found_date_index,found_datetime in enumerate(found_datetime_objs)]
			found_partial_name_list = [tuple([found_partial_name, index ]) for index,found_partial_name in enumerate(partial_name_list)]
			
			
			[db_ptr.execute("Insert into found_dobs values (%s,%s)", element) for element in found_DOB_list]
			
			[db_ptr.execute("Insert into found_partial_names values (%s,%s)", element) for element in found_partial_name_list]
			
			db_ptr.execute("""select * from iclinic_data, found_dobs, found_partial_names 
								where   found_dobs.dob = iclinic_data.dob
								and (lower(found_partial_names.partial_name) = lower(iclinic_data.first_name) or lower(found_partial_names.partial_name)=lower(iclinic_data.last_name));""") 
			ret_list = db_ptr.fetchall()
			db_ptr.execute("DROP table found_dobs;")
			db_ptr.execute("DROP table found_partial_names;")
			if len(ret_list) ==0:
				return None
			else:
				return ret_list

def main():
	connection_ptr = make_connection_to_db("test_patients", "teb8")
	#insert_patient_into_db(connection_ptr, ("1234569894","Psycooo","PGGG",datetime.date(year = 2018, month = 5, day = 18)), "iclinic_data")
	select_all(connection_ptr, "iclinic_data")
	test_found_phns = ["1234567894","1234567890","1234567896"]
	test_found_DOBs = [datetime.date(year = 1994, day = 4, month = 10)]
	test_found_part_names = ["Bez Thomas", "Melvin"]
	print("PHN_vs_DOB_vs_partial_name_query", PHN_vs_DOB_vs_partial_name_query(connection_ptr, test_found_phns,test_found_DOBs, test_found_part_names, "iclinic_data"))
	print("PHN_vs_DOB_query", PHN_vs_DOB_query(connection_ptr, test_found_phns,test_found_DOBs,"iclinic_data"))
	print("PHN_vs_partial_name_query", PHN_vs_partial_name_query(connection_ptr, test_found_phns,test_found_part_names,"iclinic_data"))
	print("DOB_vs_partial_name_query", DOB_vs_partial_name_query(connection_ptr, test_found_DOBs,test_found_part_names,"iclinic_data"))



	connection_ptr.close()


if __name__ == "__main__":
	main()

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



import datetime
from pg import DB

##################Simple initialize function for a pointer to a database

def make_connection_to_db(database_name):	
	try:
		return DB(database_name)
	except:
		print("database named {} not found in system.".format(database_name))
		return


This function is meant to enter a single patient/row into a table called public.patients, to a patients table stored within a specified database
Inputs: db_ptr: a pointer to a PyGreSQL database object. 
				Must contain the table: "public.patients" with the columns/attributes: {dob: datetime.date},{phn:str},{first_name:str},{last_name:str}
		new_patient_first_name: string object, specifiying the first name of the patient
		new_patient_last_naem: string object specifying the last name of the patient
		new_patient_phn: string object, unique and primary key for the rows in the table
		new_patient_dob_datetime_obj: datetime.date object, which represents the dob of the new patient

def insert_patient_into_db(db_ptr, new_patient_first_name,new_patient_last_name,new_patient_dob_datetime_obj,new_patient_phn):
	
	try:
		assert "public.iclinic_data" in db_ptr.get_tables()
	except AssertionError:
		print("could not find public.iclinic_data db in patient_data on system")
		return
	try:
		assert "dob" and "phn" and "first_name" and "last_name" in db_ptr.get_attnames("public.iclinic_data")
	except AssertionError:
		print("could not find required column names: dob, phn, first_name, or last_name")
		return
	try:
		db_ptr.insert("public.iclinic_data",first_name=new_patient_first_name, last_name= new_patient_last_name,dob = new_patient_dob_datetime_obj,phn = new_patient_phn)
	except:
		print("phn {} already exists in database, cannot insert a duplicate".format(new_patient_phn))
	return

Basically the above function, but for DB.inserttable, not DB.insert

def insert_patient_tuples_into_db(db_ptr, patient_tuples):
	#tuples are of the form: (new_patient_phn,new_patient_first_name,new_patient_last_name,new_patient_dob_datetime_obj)
	try:
		assert "public.iclinic_data" in db_ptr.get_tables()
	except AssertionError:
		print("could not find public.iclinic_data db in patient_data on system")
		return
	try:
		assert  "phn" and "first_name" and "last_name" and "dob" in db_ptr.get_attnames("public.iclinic_data")
	except AssertionError:
		print("could not find required column names: dob, phn, first_name, or last_name")
		return
	db_ptr.inserttable("public.iclinic_data",patient_tuples)
	return

FUNCTION: PHN_vs_DOB_vs_partial_name_query(db_ptr, found_PHNs, found_datetime_objs, found_names)
IDea: check the database to find a match of 
def PHN_vs_DOB_vs_partial_name_query(db_ptr, found_PHNs, found_datetime_objs, found_full_names):
	if len(found_PHNs) == 0 or len(found_datetime_objs) == 0 or len(found_full_names)==0:
		return None
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
	ret_val =  db_ptr.query(select * from iclinic_data, found_phns, found_dobs, found_partial_names 
								where iclinic_data.phn=found_phns.phn and found_dobs.dob = iclinic_data.dob
								and (lower(found_partial_names.partial_name) = lower(iclinic_data.first_name) or lower(found_partial_names.partial_name)=lower(iclinic_data.last_name));) 
	#dropping the tables we made to crossreference DOB vs PHN in the public.patients table
	db_ptr.query("DROP TABLE found_phns;")
	db_ptr.query("DROP TABLE found_dobs;")
	db_ptr.query("DROP TABLE found_partial_names;")
	if len(ret_val.getresult())== 0 :
		return None
	return ret_val
	
	
	
	
	
Function: PHN_vs_DOB_query
Idea: meant to check a table called "public.patients" for any rows which contain a phn from a python list object, as well as an equal date in the form of a 
	  datetime.date object, with the intention of identifying the patient referenced in the medical letter by finding a match in both attributes.

Input:db_ptr: a PyGreSQL pointer to a db object on the local system
	  found_PHNs: a python list of 10 digit strings, representing all 10 digit numbers found in the medical letter pdf
	  found_DOBs_datetime_obj: a list of datetime.date objects, representing all the dates found in the medical letter pdf

Output: returns a string which represents rows from the public.patients table which contains both a PHN and DOB match from a SQL query
	   

def PHN_vs_DOB_query(db_ptr, found_PHNs, found_datetime_objs):
	if len(found_PHNs) == 0 or len(found_datetime_objs) == 0:
		return None
	
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
	ret_val =  db_ptr.query(select * from iclinic_data, found_phns, found_dobs
									where iclinic_data.phn=found_phns.phn and found_dobs.dob = iclinic_data.dob;) 
	#dropping the tables we made to crossreference DOB vs PHN in the public.patients table
	db_ptr.query("DROP TABLE found_phns;")
	db_ptr.query("DROP TABLE found_dobs;")
	if len(ret_val.getresult())== 0 :
		return None
	return ret_val
FUNCTION: PHN_vs_partial_name(db_ptr,found_PHNs,found_full_names)
IDEA: given the names and potential (10 digit) PHNs found in a pdf document, check to see if any of the patients in the patient database
		contains one of the found PHNs, as well as a first (inclusive)or last name match with the found names in the document. Both found_PHNs and 
		found_full_names
def PHN_vs_partial_name_query(db_ptr, found_PHNs, found_full_names):
	if len(found_PHNs) == 0 or len(found_full_names) == 0:
		return None
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
	ret_val = db_ptr.query(SELECT * from public.iclinic_data, public.partial_names, public.found_phns
								where (lower(partial_names.part_name) = lower(iclinic_data.first_name) or lower(partial_names.part_name)=lower(iclinic_data.last_name))
									and (public.iclinic_data.phn = found_phns.found_phn); )
	#print(db_ptr.query("SELECT * from partial_names"))
	#print(db_ptr.query("SELECT * from found_phns"))
	db_ptr.query("DROP table partial_names;")
	db_ptr.query("DROP table found_phns;")
	if len(ret_val.getresult())== 0 :
		return None
	return ret_val
	
def DOB_vs_partial_name_query(db_ptr, found_datetime_objs, found_full_names):
	if len(found_datetime_objs) == 0 or len(found_full_names) == 0:
		return None
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
	ret_val =  db_ptr.query(select * from iclinic_data, found_dobs, found_partial_names 
								where found_dobs.dob = iclinic_data.dob
								and (lower(found_partial_names.partial_name) = lower(iclinic_data.first_name) or lower(found_partial_names.partial_name)=lower(iclinic_data.last_name));) 
	#dropping the tables we made to crossreference DOB vs partial name match in the public.patients table
	
	db_ptr.query("DROP TABLE found_dobs;")
	db_ptr.query("DROP TABLE found_partial_names;")
	if len(ret_val.getresult())== 0 :
		return None
	return ret_val	
def PHN_query(db_ptr, found_PHNs):
	if len(found_PHNs) == 0:
		return None
	try:
		db_ptr.query("CREATE TABLE found_phns(found_phn text PRIMARY KEY, phn_index INTEGER UNIQUE)")
	except:
		db_ptr.query("DROP TABLE found_phns")
		db_ptr.query("CREATE TABLE found_phns(found_phn text PRIMARY KEY, phn_index INTEGER UNIQUE)")
	
	#the tables are made now
	
	found_PHN_table = [tuple([x,phn_index]) for phn_index,x in enumerate(found_PHNs)]
	db_ptr.inserttable("public.found_phns", found_PHN_table)
	ret_val = db_ptr.query(SELECT * from public.iclinic_data, public.found_phns
								where (public.iclinic_data.phn = found_phns.found_phn); )
	#print(db_ptr.query("SELECT * from partial_names"))
	#print(db_ptr.query("SELECT * from found_phns"))
	
	db_ptr.query("DROP table found_phns;")
	if len(ret_val.getresult())== 0 :
		return None
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

"""
