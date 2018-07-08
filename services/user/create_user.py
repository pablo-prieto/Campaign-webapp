import sys
import os
import datetime
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import base_cmd.db_commands as db
import base_cmd.generic_commands as gc


def check_username_pass(cur, table, email, phone, password):
	for char in email:
		email = email.lower()
		if not char.isalpha() and char != "@" and char != ".":
			return "Email contains invalid characters."
	if not any(word in email for word in [".edu", ".com", ".net", ".org", ".gov"]) and email.count("@") != 1:
		return "Email is not valid or incorrectly formated."
			
	duplicate = (db.exist_items(cur, table, email = gc.quote(email)) or 
		db.exist_items(cur, table, phone = gc.quote(phone)))
	if duplicate:
		return "User account exists"
		
	if len(password) < 8 or len(password) > 16:
		return "Password must be between 8 and 16"


def send_user_db(cur, status, usertype, comp_name, name, borough, state, phone, email, password, salt, reg_date):
	"""
	Will create an account in the database
	args: all strings
	returns: none
	"""
	db.insert_tb(cur, "user_cred", status=gc.quote(status), usertype=gc.quote(usertype),
		comp_name=gc.quote(comp_name), name=gc.quote(name), borough=gc.quote(borough), state=gc.quote(state),
		phone=gc.quote(phone), email = gc.quote(email), password = gc.quote(password), salt = gc.quote(salt),
		reg_date=gc.quote(reg_date))
		
def insert_other_tb(cur, user_id):
	"""
	Will create other relative tables from user
	args: cur (address), user_id (int)
	returns: none
	"""
	db.insert_tb(cur, "profiles", user_id = user_id, picture_id = "", about = "")
	db.insert_tb(cur, "configs", user_id = user_id)
	# will send a request of approval to admin
	db.insert_tb(cur, "approval_queue", queued_id = user_id)
		
def setup_user(cur, usertype, comp_name, name, borough, state, phone, email, password):
	"""
	Will setup appropriate information of the user
	args: all strings
	returns: none
	"""
	status = "inactive"
	password, salt = gc.hash_pass(password)
	reg_date = datetime.datetime.today().strftime('%Y-%m-%d')
	send_user_db(cur, status, usertype, comp_name, name, borough, state, phone, email, password, salt, reg_date)
	
	sql = "SELECT user_id FROM user_cred WHERE email = '%s' and comp_name = '%s'" % (email, comp_name)
	cur.execute(sql)
	user_id = cur.fetchone()[0]
	
	insert_other_tb(cur, user_id)

def create_user(usertype, comp_name, name, borough, state, phone, email, password):
	"""
	The main function for user creation.
	args: all strings
	returns: results (dictionary)
	"""
	remote = False
	con, cur, valid_tables = gc.general_setup(remote, usertype)
	
	# check if table exists
	if not valid_tables:
		return gc.results(con, cur, "0", "Table has not yet been created")
	
	message = check_username_pass(cur, "user_cred", email, phone, password)
	if message:
		return gc.results(con, cur, "0", message)
		
	setup_user(cur, usertype, comp_name, name, borough, state, phone, email, password)
	return gc.results(con, cur, "1")	
##########################################################################


def send_admin_db(cur, usertype, name, phone, email, password, salt, reg_date):
	"""
	Will create an account in the database
	args: all strings
	returns: none
	"""
	db.insert_tb(cur, "admin_cred", usertype=gc.quote(usertype), name=gc.quote(name), phone=gc.quote(phone),
		email = gc.quote(email), password = gc.quote(password), salt = gc.quote(salt), reg_date=gc.quote(reg_date))
	
def setup_admin(cur, name, phone, email, password):
	"""
	Will setup appropriate information of the admin.
	args: all strings
	returns: none
	"""
	password, salt = gc.hash_pass(password)
	reg_date = datetime.datetime.today().strftime('%Y-%m-%d')
	send_admin_db(cur, "admin", name, phone, email, password, salt, reg_date)

def create_admin(usertype, name, phone, email, password):
	"""
	The main function for admin creation.
	args: all strings
	returns: results (dictionary)
	"""
	remote = False
	con, cur, valid_tables = gc.general_setup(remote, usertype)
	
	# check if table exists
	if not valid_tables:
		return gc.results(con, cur, "0", "Table has not yet been created")

	message = check_username_pass(cur, "admin_cred", email, phone, password)
	if message:
		return gc.results(con, cur, "0", message)
	
	setup_admin(cur, name, phone, email, password)
	return gc.results(con, cur, "1")

	
	
# print(create_user("influencer", "banana", "banana", "Manhattan", "NY", "718-239-4738", "banana@b.", "bananahana"))
#print(create_admin("banana", "718-239-4738", "banana@b.", "bananahana"))