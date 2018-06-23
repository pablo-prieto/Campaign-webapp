import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import base_cmd.db_commands as db
import base_cmd.generic_commands as gc

def validate_user(cur, actor, email, password):
	# check if table exists
	if not gc.check_tb_relations(cur, actor):
		return gc.val_results(con, cur, "0", "false", "Table has not yet been created")
	table = actor + "_cred"
	
	hashpassword = gc.hash_login_pass(cur, table, email, password)
	
	cur.execute("SELECT user_id FROM %s WHERE email = '%s' and password = '%s'" % (table, email, hashpassword))
	value = cur.fetchone()
	return value

def login(email, password):
	"""
	Returns user id given the email and password
	"""
	remote = False
	con, cur = gc.setup_db(remote)
	
	value = validate_user(cur, "admin", email, password)
	if value: # we know admin was able to login
		return gc.val_results(con, cur, "1", value[0], "true")
	
	value = validate_user(cur, "user", email, password)
	if value: # else we know that a user was able to login
		# check if user's account has been activated by admin
		cur.execute("SELECT status FROM user_cred WHERE user_id = %s" % (value[0],))
		if cur.fetchone()[0] == "inactive":
			return gc.val_results(con, cur, "0", "NULL", "false", "User's information has yet to be confirmed")
		return gc.val_results(con, cur, "1", value[0], "false")
	
	# else if still does not exist, there is no such credentials
	return results(con, cur, "0", "NULL", "false", "Wrong email and/or password")
	
##################################################################################################
	
def get_value(cur, actor, table, user_id, key):
	"""
	Returns a value and the correct status (admin or user) of the user.
	args: cur (address), status (string), user_id(string), key (string)
	returns: value (any), status (string)
	"""
	status = False
	cur.execute("SELECT %s FROM %s WHERE user_id = %s" % (key, table, user_id))
	value = cur.fetchone()
	if value:
		value = value[0]
		if actor == "admin":
			status = "true"
	else:
		value = "NULL"
	return value, status
	
def get_one(con, cur, actor, user_id, key):
	"""
	Returns selected information of the user.
	args: con (address), cur (address), status (string), user_id(string), key (string)
	returns: dictionary
	"""
	# find out table which table we want
	table = gc.find_table(actor, key)
	if not table:
		return gc.val_results(con, cur, "0", "NULL", "false", "no such actor and key combination")
		
	value, status = get_value(cur, actor, table, user_id, key)
	return gc.val_results(con, cur, "1", value, status)
	
###########################################
	
def get_values(cur, values, actor, table, user_id):
	"""
	Returns a value and the correct status (admin or user) of the user.
	args: cur (address), status (string), user_id(string)
	returns: value (any), status (string)
	"""
	status = False
	if actor == "admin":
		if table == "admin_cred":
			values["name"] = db.get_item(cur, table, "user_id", user_id, "name")
			values["phone"] = db.get_item(cur, table, "user_id", user_id, "phone")
			values["email"] = db.get_item(cur, table, "user_id", user_id, "email")
			values["reg_date"] = db.get_item(cur, table, "user_id", user_id, "reg_date")
			values["admin"] = "true"
		elif table == "approval_queue":
			cur.execute("SELECT DISTINCT user_id FROM approval_queue")
			values["user_ids"] = list(list(zip(*cur.fetchall()))[0])
	else:
		if table == "user_cred":
			values["status"] = db.get_item(cur, table, "user_id", user_id, "status")
			values["usertype"] = db.get_item(cur, table, "user_id", user_id, "usertype")
			values["comp_name"] = db.get_item(cur, table, "user_id", user_id, "comp_name")
			values["name"] = db.get_item(cur, table, "user_id", user_id, "name")
			values["borough"] = db.get_item(cur, table, "user_id", user_id, "borough")
			values["state"] = db.get_item(cur, table, "user_id", user_id, "state")
			values["phone"] = db.get_item(cur, table, "user_id", user_id, "phone")
			values["email"] = db.get_item(cur, table, "user_id", user_id, "email")
			values["reg_date"] = db.get_item(cur, table, "user_id", user_id, "reg_date")
			values["admin"] = "false"
		elif table == "profiles":
			values["picture_id"] = db.get_item(cur, table, "user_id", user_id, "picture_id")
			values["about"] = db.get_item(cur, table, "user_id", user_id, "about")
		elif table == "configs":
			pass
		elif table == "user_interests":
			cur.execute("SELECT interests FROM %s WHERE user_id = %s" % (table, user_id))
			val = cur.fetchall()
			if val:
				values["interests"] = list(list(zip(*val))[0])
			else:
				values["interests"] =  []
		elif table == "user_favorites":
			cur.execute("SELECT favorites FROM %s WHERE user_id = %s" % (table, user_id))
			val = cur.fetchall()
			if val:
				values["favorites"] = list(list(zip(*val))[0])
			else:
				values["favorites"] = []
		elif table == "campaigns":
			values["campaigns"] = []
			campaign = {}
			cur.execute("SELECT DISTINCT campaign_id FROM %s WHERE user_id = %s" % (table, user_id))
			val = cur.fetchall()
			if val:
				ids = list(list(zip(*val))[0])
				for id in ids:
					campaign["user_id"] = db.get_item(cur, table, "campaign_id", id, "user_id")
					campaign["campaign_name"] = db.get_item(cur, table, "campaign_id", id, "campaign_name")
					campaign["tags"] = db.get_item(cur, table, "campaign_id", id, "tags")
					campaign["create_date"] = db.get_item(cur, table, "campaign_id", id, "create_date")
					campaign["rating"] = db.get_item(cur, table, "campaign_id", id, "rating")
					campaign["review"] = db.get_item(cur, table, "campaign_id", id, "review")
					campaign["reviewer"] = db.get_item(cur, table, "campaign_id", id, "reviewer")
					values["campaigns"].append(campaign)
		elif table == "user_titles":
			values["user_titles"] = []
			titles = {}
			cur.execute("SELECT DISTINCT title_id FROM %s WHERE user_id = %s" % (table, user_id))
			val = cur.fetchall()
			if val:
				ids = list(list(zip(*val))[0])
				for id in ids:
					titles["title_id"] = db.get_item(cur, table, "user_id", id, "user_id")
					titles["date"] = db.get_item(cur, table, "user_id", id, "campaign_name")
					values["user_titles"].append(titles)
	return values
	
def get_all(con, cur, actor, user_id):
	"""
	Returns all information of the user.
	args: con (address), cur (address), status (string), user_id(string)
	returns: dictionary
	"""
	tables = gc.get_all_tb(actor)
	values = {"success":"1", "reason":""}
	
	for table in tables:
		values = get_values(cur, values, actor, table, user_id)
	return values
###########################################
	
def get_user_info(actor, user_id, key):
	"""
	Returns a generic get method for either get all or one for user
	args: actor (string), user_id (string), key (string)
	returns: results (dictionary)
	"""
	remote = False	
	con, cur = gc.setup_db(remote)
	
	# check related tables exist
	if not gc.check_tb_relations(cur, actor):
		return gc.val_results(con, cur, "0", "NULL", "false", "Necessary tables have not yet been created")
	
	if key == "all":
		return get_all(con, cur, actor, user_id)
	else:
		return get_one(con, cur, actor, user_id, key)

# print(login("banana@b.", "bananahana"))
# print(get_user_info("user","1", "name"))
# print(get_user_info("user","4", "all"))