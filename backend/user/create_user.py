import sys
import os
import datetime
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import base_cmd.db_commands as db
import base_cmd.generic_commands as gc


def send_user_db(cur, istatus, iusertype, icomp_name, iname, iborough, istate, iphone, iemail, ipassword, isalt, ireg_date):
	"""
	Will create an account in the database
	args: all strings
	returns: none
	"""
	db.insert_tb(cur, "user_cred", status=gc.quote(istatus), usertype=gc.quote(iusertype),
		comp_name=gc.quote(icomp_name), name=gc.quote(iname), borough=gc.quote(iborough), state=gc.quote(istate),
		phone=gc.quote(iphone), email = gc.quote(iemail), password = gc.quote(ipassword), salt = gc.quote(isalt),
		reg_date=gc.quote(ireg_date))
		
def insert_other_tb(cur, iuser_id):
	"""
	Will create other relative tables from user
	args: cur (address), iuser_id (int)
	returns: none
	"""
	db.insert_tb(cur, "profiles", user_id=iuser_id, picture_id="", about="")
	db.insert_tb(cur, "configs", user_id=iuser_id)
	# will send a request of approval to admin
	db.insert_tb(cur, "approval_queue", user_id=iuser_id)
		
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
	con, cur, valid_tables = gc.general_setup(remote, "user")
	
	# check if table exists
	if not valid_tables:
		return gc.results(con, cur, "0", "Table has not yet been created")
	
	if len(password) < 8 or len(password) > 16:
		return gc.results(con, cur, "0", "Password must be between 8 and 16")
			
	duplicate = db.exist_items(cur, 'user_cred', email = gc.quote(email))
	if duplicate:
		return gc.results(con, cur, "0", "User account exists")
		
	setup_user(cur, usertype, comp_name, name, borough, state, phone, email, password)
	return gc.results(con, cur, "1")	
##########################################################################


def send_admin_db(cur, iname, iphone, iemail, ipassword, isalt, ireg_date):
	"""
	Will create an account in the database
	args: all strings
	returns: none
	"""
	db.insert_tb(cur, "admin_cred", name=gc.quote(iname), phone=gc.quote(iphone), email = gc.quote(iemail),
		password = gc.quote(ipassword), salt = gc.quote(isalt), reg_date=gc.quote(ireg_date))
	
def setup_admin(cur, name, phone, email, password):
	"""
	Will setup appropriate information of the admin.
	args: all strings
	returns: none
	"""
	password, salt = gc.hash_pass(password)
	reg_date = datetime.datetime.today().strftime('%Y-%m-%d')
	send_admin_db(cur, name, phone, email, password, salt, reg_date)

def create_admin(name, phone, email, password):
	"""
	The main function for admin creation.
	args: all strings
	returns: results (dictionary)
	"""
	remote = False
	con, cur, valid_tables = gc.general_setup(remote, "admin")
	
	# check if table exists
	if not valid_tables:
		return gc.results(con, cur, "0", "Table has not yet been created")
			
	if len(password) < 8 or len(password) > 16:
		return gc.results(con, cur, "0", "Password must be between 8 and 16")
	
	duplicate = db.exist_items(cur, 'admin_cred',email = gc.quote(email))
	if duplicate:
		return gc.results(con, cur, "0", "User account exists")
		
	setup_admin(cur, name, phone, email, password)
	return gc.results(con, cur, "1")

	
	
# print(create_user("influencer", "banana", "banana", "Manhattan", "NY", "718-239-4738", "banana@b.", "bananahana"))
#print(create_admin("banana", "718-239-4738", "banana@b.", "bananahana"))