import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import base_cmd.db_commands as db
import base_cmd.generic_commands as gc

def username_option(cur, table, user_id, key, value):
	"""
	Will update email
	args:
	returns: message (string)
	"""
	if key == 'email':
		value = value.lower()
		for char in value:
			if not char.isalpha() and char != "@" and char != ".":
				return "Email contains invalid characters"
		if not any(word in value for word in [".edu", ".com", ".net", ".org", ".gov"]) and value.count("@") != 1:
			return "Email is not valid or incorrectly formated."
	if db.exist_items(cur, table, key=gc.quote(value)):
		return "Username already exists"
		
	db.update_tb(cur, table, "user_id", user_id, key, gc.quote(value))
	return ""
	
	
def password_option(cur, table, user_id, key, value):
	"""
	Will update password
	args:
	returns: message (string)
	"""
	if len(value) < 8 or len(value) > 16:
		return "Password must be between 8 and 16"
		
	value, salt = gc.hash_pass(value)
	db.update_tb(cur, table, "user_id", user_id, key, gc.quote(value))
	db.update_tb(cur, table, "user_id", user_id, "salt", gc.quote(value))
	return ""

def about_option(cur, table, user_id, key, value):
	"""
	Will update about part of the user
	args:
	returns: message (string)
	"""
	if len(value) > 256:
		return "Sentence too long"
	db.check_profile_exist(user_id)
	db.update_tb(cur, table, "user_id", user_id, key, gc.quote(value))
	return  ""
	
	
def other_option(cur, table, user_id, key, value):
	"""
	Will update all user generic cases
	args:
	returns: message (string)
	"""
	db.update_tb(cur, table, "user_id", user_id, key, gc.quote(value))
	return ""

def update_user(user_id, key, value):
	"""
	Will update user
	args: usertype (string), user_id (int), key (string), value (any)
	returns: dictionary
	"""
	con, cur = gc.setup_db()
		
	# find out table which table we want
	table = gc.find_table(cur, "user", user_id, key)
	if not table:
		return gc.results(con, cur, "0", "no such key")
		
	if key == 'email' or key == 'phone':
		message = username_option(cur, table, user_id, key, value)
	elif key == 'password':
		message = password_option(cur, table, user_id, key, value)
	elif key == "about":
		message = about_option(cur, table, user_id, key, value)
	else:
		message = other_option(cur, table, user_id, key, value)
		
	if message:
		return gc.results(con, cur, "0", message)
	else:
		return gc.results(con, cur, "1")
		
def approve_user(user_id, status):
	"""
	Will approve user
	args: user_id (int)
	returns: dictionary
	"""
	con, cur = gc.setup_db()
	
	# check related tables exist
	
	db.del_row(cur, "user_queue", "user_id", int(user_id))
	db.update_tb(cur, "credentials", "user_id", user_id, "status", gc.quote(status))
	return gc.results(con, cur, "1")
	
# print(update_user("4", "usertype", "business"))