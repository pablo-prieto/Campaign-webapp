import hashlib, uuid
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import base_cmd.db_commands as db

def setup_db():
	"""
	This function will connect to the database and setup the table features and will also clear any old data.
	args: none
	returns: con (address), cur (address)
	"""
	print('Connecting to database...')
	# function from db_commands to connect to database
	con, cur = db.connect()
	return con, cur

def close_db(con, cur):
	"""
	Closes the database
	args: con (address), cur (address)
	returns: none
	"""
	db.end(con, cur)

def get_all_tb(field):
	if field == 'influencer':
		return ['credentials', 'profiles', 'configs', 'user_tags', 'user_titles', 'influencer_platforms', 'user_favorites', 'affiliated_campaigns']
	elif field == 'business':
		return ['credentials', 'profiles', 'configs', 'user_tags', 'user_titles', 'businesses', 'campaigns', 'images', 'approval_queue']
	elif field == 'admin':
		return ['credentials', 'user_queue']
	elif field == 'topics':
		return ['tags', 'titles', 'styles', 'platforms']
	elif field == 'campaigns':
		return ['campaigns', 'images', 'campaign_tags', 'approval_queue']
	else:
		return []
	
def check_tb_relations(cur, usertype):
	"""
	Will check if the table and its relative table exist
	args: cur (address), usertype (string)
	returns: boolean
	"""
	if usertype == 'admin':
		return db.exist_tb(cur, 'credentials')
	elif usertype == 'user':
		return (db.exist_tb(cur, 'credentials') and db.exist_tb(cur, 'user_queue')
			and db.exist_tb(cur, 'profiles') and db.exist_tb(cur, 'configs'))
	elif usertype == 'business':
		return (db.exist_tb(cur, 'credentials') and db.exist_tb(cur, 'profiles')
			and db.exist_tb(cur, 'configs')
			and db.exist_tb(cur, 'campaigns') and db.exist_tb(cur, 'images'))
	elif usertype == 'influencer':
		return (db.exist_tb(cur, 'credentials') and db.exist_tb(cur, 'profiles')
			and db.exist_tb(cur, 'configs')
			and db.exist_tb(cur, 'affiliated_campaigns') and db.exist_tb(cur, 'user_favorites'))
	else:
		return False
	
def general_setup(usertype):
	"""
	Will connect to the database and check if the relative table exists
	args: usertype (string)
	returns: con (address), cur (address), boolean
	"""
	con, cur = setup_db()
	return con, cur, check_tb_relations(cur, usertype)
	
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
def get_usertype(cur, user_id):
	return db.get_item(cur, 'credentials', 'user_id', user_id, 'usertype')

def find_table(cur, topic, user_id, key):
	"""
	Finds the table correspoding to the usertype (user, admin) and key (attribute)
	args: cur, topic, user_id, key
	returns: table (string)
	"""
	usertype = get_usertype(cur, user_id)
	if topic == 'user':
		if usertype == 'admin':
			table = 'credentials'
		elif usertype == 'business' or 'influencer':
			if key in ('status', 'usertype', 'first_name', 'last_name', 'borough', 'state', 'phone', 'email', 'password'):
				table = 'credentials'
			elif key in ('pic_url', 'active_tag_id', 'about'):
				table = 'profiles'
			elif key in ('tags'):
				table = 'user_tags'
			elif key in ('title_id'):
				table = 'user_titles'
			else:
				table = None
	elif topic == 'professions':
		if usertype == 'business':
			if key in ('campaigns'):
				table = 'campaigns'
			elif key in ('images'):
				table = 'images'	
			else:
				table = None
		elif usertype == 'influencer':
			if key in ('affil_id'):
				table = 'affiliated_campaigns'
			elif key in ('favorites'):
				table = 'user_favorites'
			else:
				table = None
		else:
			table = None
	else:
		table = None
	return table
	
def results(con, cur, success, reason = ''):
	"""
	Will print a generic result in json format
	args: con (address), cur (address), success (string), reason (string)
	returns: dictionary
	"""
	close_db(con, cur)
	print('rebuild finished successfully.')
	return {'success': success, 'reason':reason}
	
def val_results(con, cur, success, val, usertype, reason = ''):
	close_db(con, cur)
	print('rebuild finished successfully.')
	return {'success': success, 'value': val, 'usertype': usertype, 'reason':reason}
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

def hash_login_pass(cur, table, login_type, username, password):
	"""
	Will create a hashed password from a given user salt
	args: cur (address), table (string), login_type(string), username(string), password (string)
	returns: password(string)
	"""
	cur.execute("SELECT salt FROM %s WHERE %s = '%s'" % (table, login_type, username))
	value = cur.fetchone()
	if not value:
		return 0
	salt = value[0]
	password = hashlib.sha512((password + salt).encode('utf-8')).hexdigest()
	return password