# DESCRIPTION: This is like support functions for SQL commands
# Author: Eun Il Kim

import psycopg2
import decimal
import sys
import os

# This contains the login for the database, make your own...
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
import aws_config.info as info

# Make sure you comment out <"import aws_config.info as info"> for local

###############################################################################################################################
# GENERIC FUNCTIONS

def connect(remote = True):
	"""
	connects to the database
	args: remote (boolean)
	returns: con, cur (addresses)
	"""
	remote = True
	if remote:
		host = info.host
		dbname = info.dbname
		user = info.user
		password = info.password
	else: # local
		host = 'localhost'
		dbname = 'users'
		user = 'postgres'
		password = 'postgre'

	con = psycopg2.connect("host='%s' dbname='%s' user='%s' password='%s'" %(host, dbname, user, password))   
	cur = con.cursor()
	return con, cur

def end(con, cur):
	"""
	Commits all changes and closes the connection, making sure there is no errors.
	Otherwise it will print the database error.
	args: con, cur (addresses)
	returns: errors if any
	"""
	try:
		con.commit()
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if con is not None:
			con.close()
			
def exist_tb(cur, table_name):
	"""
	This is a generic function that will check if table exists
	args: cur(address), table_name (string)
	returns: true or false
	"""
	cur.execute("SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name = '%s')" % (table_name,))
	return cur.fetchone()[0]

def create_tb(cur, table_name, primary_key_nums, **kwargs):
	"""
	This is a generic function that will create a new table in the database
	args: cur (address), table_name (string),
		primary_key_nums: indicates the amount of primary keys(int),
		**kwargs contain kwargs[name] = type (dictionary)
	returns: nothing
	"""
	sql = "CREATE TABLE %s (" % (table_name,)
	if primary_key_nums == 1:
		for key in kwargs:
			if primary_key_nums:
				sql += "%s %s PRIMARY KEY" % (key, kwargs[key])
				primary_key_nums = 0
			else:
				sql += ", %s %s" % (key, kwargs[key])
		sql += ")"
	else: #if composite primary keys...
		for key in kwargs:
			sql += "%s %s, " % (key, kwargs[key])
		sql += "PRIMARY KEY ("
		for key in list(kwargs.keys())[0:primary_key_nums]:
			sql += str(key) + ", "
		sql = sql[:-2] + "))"
	cur.execute(sql)
	
def insert_tb(cur, table_name, **kwargs):
	"""
	This generic function will insert new values inside a table.
	args: cur (address), table_name (string),
		*kwargs is a collection of objects (list)
	returns: nothing
	"""
	sql = "INSERT INTO %s (" % (table_name,)
	for key in kwargs:
		sql += "%s, " % (key,)
	sql = sql[:-2] + ") VALUES("
	for key in kwargs:
		if kwargs[key] == '':
			sql+= "NULL, " 
		else:
			sql += "%s, " % (kwargs[key],)
	sql = sql[:-2] + ")"
	cur.execute(sql)
	
def update_tb(cur, table_name, key_name, key_value, target, value):
	"""
	This generic function will replace any value with a give a given value
	args: cur (address), table_name (string), key_name (string), key_value (object),
		target (string) is the column you are interested in, value (object)
	returns: nothing
	"""
	cur.execute("UPDATE %s SET %s=%s WHERE %s=%s" % (table_name, target, value, key_name, key_value))

def del_tb(cur, table_name):
	"""
	This generic function deletes the desired table
	args: cur (address), table_name (string)
	returns: nothing
	"""
	cur.execute("DROP TABLE IF EXISTS %s" % (table_name, ))
	
def del_row(cur, table_name, key, value):
	"""
	This generic function deletes the desired row
	args: cur (address), table_name (string), key (string)
	returns: nothing
	"""
	cur.execute("DELETE FROM %s WHERE %s= %s" % (table_name, key, value))
	
def exist_items(cur, table_name, **kwargs):
	"""
	This is a generic function that will check if the input is not duplicate
	args: cur (address), table_name (string),
		**kwargs contain kwargs[name] = type (dictionary)
	returns: true or false
	"""
	sql = "SELECT EXISTS (SELECT * FROM %s WHERE " % (table_name,)
	for key in kwargs:
		sql += "%s = %s AND " % (key, kwargs[key])
	sql = sql[:-5] + ")"
	cur.execute(sql)
	return cur.fetchone()[0]

def get_item(cur, table_name, id_name, id, *args):
	"""
	This is a generic function that will check if the input is not duplicate
	args: cur (address), table_name (string),
		**kwargs contain kwargs[name] = type (dictionary)
	returns: true or false
	"""
	sql = "SELECT "
	for keys in args:
		if keys:
			sql += keys + ", "
	sql = sql[:-2] + " FROM %s WHERE %s = %s " % (table_name, id_name, id)
	cur.execute(sql)
	
	if len(args) == 1:
		value = cur.fetchone()
		if value == None:
			return "NULL"
		return value[0]
	else:
		value = cur.fetchall()
		if value[0][0] == None:
			return "NULL"
	return value
	
def distinct_items(cur, table_name, key, id_name = None, id = None):
	"""
	This is a generic function that will check if the input is not duplicate
	args: cur (address), table_name (string),
		**kwargs contain kwargs[name] = type (dictionary)
	returns: true or false
	"""
	if id_name:
		sql = "SELECT DISTINCT %s FROM %s WHERE %s = %s" % (key, table_name, id_name, id)
	else:
		sql = "SELECT DISTINCT %s FROM %s" % (key, table_name)
	cur.execute(sql)

	value = cur.fetchall()
	if value:
		return list(list(zip(*value))[0])
	return None
	
def convert(item):
	"""
	This will return decimal to float to be used in json
	args: item (Decimal(string))
	returns: item (float)
	"""
	if isinstance(item, decimal.Decimal):
		return float(item) 
	return item

def convert_decimal(lst_of_items):
	"""
	This will return a new list that has no decimal coordinates
	args: lst_of_items (list)
	returns: lst_of_items (list)
	"""
	return list(map(lambda items: list(map(lambda item: convert(item), items)), lst_of_items))
############################################################################################################################
# CUSTOM FUNCTIONS

# def create_user(cur, table_name, **kwargs):
	# """
	# This will create a new table for users in the database
	# args: cur (address), table_name (string),
		# **kwargs contain kwargs[name] = type (dictionary)
	# returns: nothing
	# """
	# sql = "CREATE TABLE %s (user_id SERIAL PRIMARY KEY" % (table_name,)
	# for key in kwargs:
		# sql += ", %s %s" % (key, kwargs[key])
	# sql += ")"
	# cur.execute(sql)
	
def check_profile_exist(cur, user_id):
	sql = "SELECT EXIST (SELECT * FROM profiles WHERE user_id = %s)" % (user_id,)
	cur.execute(sql)
	if cur.fetchone()[0]:
		insert_tb(user_id, '', '', '')
	
def gen_pic_id(cur, user_id):
	"""
	This will generate a image id that corresponds to the data in the database
	args: cur (address), user_id (string),
	returns: nothing
	"""
	sql = "DECLARE nextseq integer; \
	BEGIN \
		nextseq := nextval('image_id'); \
		INSERT INTO profiles (image_id) \
		VALUES (nextseq) WHERE user_id = %s;" % (user_id,)
	cur.execute(sql)
	sql = "SELECT image_id FROM profiles WHERE user_id = %s" % (user_id,)
	cur.execute(sql)
	return cur.fetchone()[0]

# example
#if __name__ == "__main__":
	#con, cur = connect('localhost', 'gtfs', 'owner', 'gr0UP5')
	#del_tb(cur, "table_name")
	#create_tb(cur,"table_name", 1, primary_key='int', col1='VARCHAR(20)', col2='VARCHAR(20)')
	#create_tb(cur,"table_name", 2, primary_key1='int', primary_key2='VARCHAR(20)', col1='VARCHAR(20)', col2='VARCHAR(20)')
	#insert_tb(cur,"table_name", "0", "'value1'", "'value2'")
	#update_tb(cur, "table_name", "primary_key", "0", "col1", "'value0'")
	#end(con, cur)