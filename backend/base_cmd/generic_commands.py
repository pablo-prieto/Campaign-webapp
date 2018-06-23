import hashlib, uuid
import base_cmd.db_commands as db

def setup_db(remote):
	"""
	This function will connect to the database and setup the table features and will also clear any old data.
	args: none
	returns: con (address), cur (address)
	"""
	print("Connecting to database...")
	# function from db_commands to connect to database
	con, cur = db.connect(remote)
	return con, cur

def close_db(con, cur):
	"""
	Closes the database
	args: con (address), cur (address)
	returns: none
	"""
	db.end(con, cur)

def get_all_tb(field):
	if field == "user":
		return ["user_cred", "profiles", "configs", "user_interests", "user_favorites", "campaigns", "user_titles"]
	elif field == "admin":
		return ["admin_cred", "approval_queue"]
	elif field == "topics":
		return ["interests", "titles"]
	elif field == "campaigns":
		return ["campaigns", "images"]
	else:
		return []
	
def check_tb_relations(cur, actor):
	"""
	Will check if the table and its relative table exist
	args: cur (address), actor (string)
	returns: boolean
	"""
	if actor == "admin":
		return db.exist_tb(cur, "admin_cred")
	if actor == "user":
		return (db.exist_tb(cur, "user_cred") and db.exist_tb(cur, "profiles")
			and db.exist_tb(cur, "configs"))
	return False
	
def general_setup(remote, actor):
	"""
	Will connect to the database and check if the relative table exists
	args: remote (boolean), actor (string)
	returns: con (address), cur (address), boolean
	"""
	con, cur = setup_db(remote)
	return con, cur, check_tb_relations(cur, actor)
	
def quote(string):
	"""
	quotes any variables that are string; also checks if there is a apostrophe and fixes it.
	args: obj
	returns: string
	"""
	i = 0
	for letter in string:
		if letter == "'":
			string = string[:i]+"'"+string[i:]
			i += 1
		i += 1
	return "'{}'".format(string)
##################################################################################################
	
def find_table(actor, key):
	"""
	Finds the table correspoding to the actor (user, admin) and key (attribute)
	args: actor(string), key (string)
	returns: table (string)
	"""
	if actor == "admin":
		table = "admin_cred"
	elif actor == "user":
		if key in ("status", "usertype", "comp_name", "name", "borough", "state", "phone", "email", "password", "reg_date"):
			table = "user_cred"
		elif key in ("picture_id", "about"):
			table = "profiles"
		elif key in ("interests"):
			table = "user_interests"
		elif key in ("favorites"):
			table = "user_favorites"
		else:
			table = None
	else:
		table = None
	return table
	
def results(con, cur, success, reason = ""):
	"""
	Will print a generic result in json format
	args: con (address), cur (address), success (string), reason (string)
	returns: dictionary
	"""
	close_db(con, cur)
	print('rebuild finished successfully.')
	return {"success": success, "reason":reason}
	
def val_results(con, cur, success, val, admin, reason = ""):
	close_db(con, cur)
	print('rebuild finished successfully.')
	return {"success": success, "value": val, "admin": admin, "reason":reason}
###############################################################################################################	
	
	
def hash_pass(password):
	"""
	Will create a hashed password and its respective salt
	args: password (string)
	returns: password(string), salt(string)
	"""
	salt = uuid.uuid4().hex
	password = hashlib.sha512((password + salt).encode('utf-8')).hexdigest()
	return password, salt	

def hash_login_pass(cur, table, email, password):
	"""
	Will create a hashed password from a given user salt
	args: cur (address), table (string), email(string), password (string)
	returns: password(string)
	"""
	cur.execute("SELECT salt FROM %s WHERE email = '%s'" % (table, email))
	value = cur.fetchone()
	if not value:
		return 0
	salt = value[0]
	password = hashlib.sha512((password + salt).encode('utf-8')).hexdigest()
	return password