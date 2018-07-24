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


def send_user_db(cur, table, status, usertype, first_name, last_name, borough, state, phone, email, password, salt, create_date):
	"""
	Will create an account in the database
	args: all strings
	returns: none
	"""
	db.insert_tb(cur, table, status=gc.quote(status), usertype=gc.quote(usertype), 
		first_name=gc.quote(first_name), last_name=gc.quote(last_name), borough=gc.quote(borough), state=gc.quote(state), 
		phone=gc.quote(phone), email = gc.quote(email),  password = gc.quote(password), salt = gc.quote(salt), 
		create_date = gc.quote(create_date))
		
def insert_other_tb(cur, user_id, create_date):
	"""
	Will create other relative tables from user
	args: cur (address), user_id (int)
	returns: none
	"""
	db.insert_tb(cur, "profiles", user_id = user_id, pic_url = "", active_tag_id = 0, about = "")
	db.insert_tb(cur, "configs", user_id = user_id)
	# will send a request of approval to admin
	db.insert_tb(cur, "user_queue", user_id = user_id, create_date = gc.quote(create_date))
	
def setup_user(cur, table, usertype, first_name, last_name, borough, state, phone, email, password):
	"""
	Will setup appropriate information of the user
	args: all strings
	returns: none
	"""
	status = "inactive"
	password, salt = gc.hash_pass(password)
	create_date = datetime.datetime.today().strftime('%Y-%m-%d')
	send_user_db(cur, table, status, usertype, first_name, last_name, borough, state, phone, email, password, salt, create_date)
	
	user_id = db.get_item(cur, table, 'email', gc.quote(email), 'user_id')
	
	if usertype != 'admin':
		insert_other_tb(cur, user_id, create_date)

	
def create_user(usertype, first_name, last_name, borough, state, phone, email, password):
	"""
	The main function for user creation.
	args: all strings
	returns: results (dictionary)
	"""
	con, cur = gc.setup_db()
	table = 'credentials'
	
	message = check_username_pass(cur, table, email, phone, password)
	if message:
		return gc.results(con, cur, "0", message)
		
	setup_user(cur, table, usertype, first_name, last_name, borough, state, phone, email, password)
	return gc.results(con, cur, "1")

	
	
#print(create_user("influencer", "banana", "banana", "Manhattan", "NY", "718-239-4738", "banana@b.", "bananahana"))
#print(create_user("admin", "banana", "banana", "Manhattan", "NY", "711-239-4738", "apple@a.", "bananahana"))