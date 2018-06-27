import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import base_cmd.db_commands as db
import base_cmd.generic_commands as gc

def validate_user(cur, usertype, username, password):
	# check if table exists
	if not gc.check_tb_relations(cur, usertype):
		return gc.val_results(con, cur, "0", "false", "Table has not yet been created")
	table = usertype + "_cred"
	
	if "@" in username:
		input_type = "email"
	else:
		input_type = "phone"
	hashpassword = gc.hash_login_pass(cur, table, input_type, username, password)
	
	cur.execute("SELECT user_id, usertype FROM %s WHERE %s = '%s' and password = '%s'" % (table, input_type, username, hashpassword))
	value = cur.fetchone()
	return value

def login(username, password):
	"""
	Returns user id given the username and password
	"""
	remote = False
	con, cur = gc.setup_db(remote)
	
	value = validate_user(cur, "admin", username, password)
	if value: # we know admin was able to login
		return gc.val_results(con, cur, "1", value[0], value[1])
	
	value = validate_user(cur, "user", username, password)
	if value: # else we know that a user was able to login
		# check if user's account has been activated by admin
		cur.execute("SELECT status FROM user_cred WHERE user_id = %s" % (value[0],))
		if cur.fetchone()[0] == "inactive":
			return gc.val_results(con, cur, "0", value[0], value[1], "User's information has yet to be confirmed")
		return gc.val_results(con, cur, "1", value[0], value[1])
	
	# else if still does not exist, there is no such credentials
	return gc.val_results(con, cur, "0", "NULL", "NULL", "Wrong username and/or password")
	
##################################################################################################
	
def get_value(cur, usertype, table, user_id, key):
	"""
	Returns a value and the correct usertype (admin or user) of the user.
	args: cur (address), usertype (string), user_id(string), key (string)
	returns: value (any), usertype (string)
	"""
	cur.execute("SELECT %s FROM %s WHERE user_id = %s" % (key, table, user_id))
	value = cur.fetchone()
	if value:
		value = value[0]
	else:
		value = "NULL"
		usertype = "NULL"
	return value, usertype
	
def get_one(con, cur, usertype, user_id, key):
	"""
	Returns selected information of the user.
	args: con (address), cur (address), usertype (string), user_id(string), key (string)
	returns: dictionary
	"""
	# find out table which table we want
	table = gc.find_table(usertype, key)
	if not table:
		return gc.val_results(con, cur, "0", "NULL", "NULL", "no such usertype and key combination")
		
	value, usertype = get_value(cur, usertype, table, user_id, key)
	return gc.val_results(con, cur, "1", value, usertype)
	
###########################################
	
def get_values(cur, values, usertype, table, user_id):
	"""
	Returns a value and the correct usertype (admin or user) of the user.
	args: cur (address), usertype (string), user_id(string)
	returns: value (any), usertype (string)
	"""
	if usertype == "admin":
		if table == "admin_cred":
			values["usertype"] = db.get_item(cur, table, "user_id", user_id, "usertype")
			values["name"] = db.get_item(cur, table, "user_id", user_id, "name")
			values["phone"] = db.get_item(cur, table, "user_id", user_id, "phone")
			values["email"] = db.get_item(cur, table, "user_id", user_id, "email")
			values["reg_date"] = db.get_item(cur, table, "user_id", user_id, "reg_date")
		elif table == "approval_queue":
			values["queued_id"] = []
			val = db.distinct_items(cur, "approval_queue", "queued_id")
			if val:
				values["queued_id"] = val
	elif usertype == "business" or usertype == "influencer":
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
		elif table == "profiles":
			values["picture_id"] = db.get_item(cur, table, "user_id", user_id, "picture_id")
			values["about"] = db.get_item(cur, table, "user_id", user_id, "about")
		elif table == "configs":
			values["configs"] = []
		elif table == "user_tags":
			values["tags"] =  []
			tags = {}
			tag_ids = db.distinct_items(cur, table, "tag_id", "user_id", user_id)
			if tag_ids:
				for tag_id in tag_ids:
					tags["tag_id"] = tag_id
					tags["tag_name"] = db.get_item(cur, "tags", "tag_id", tag_id, "tag_name")
					values["tags"].append(tags)
		elif table == "user_titles":
			values["user_titles"] = []
			titles = {}
			ids = db.distinct_items(cur, table, "title_id", "user_id", user_id)
			if ids:
				for id in ids:
					titles["title_id"] = id
					titles["title_name"] = db.get_item(cur, "titles", "title_id", id, "title_name")
					titles["title_info"] = db.get_item(cur, "titles", "title_id", id, "title_info")
					titles["title_date"] = db.get_item(cur, table, "title_id", id, "title_date")
					values["user_titles"].append(titles)
					
	if usertype == "business":
		if table == "campaigns":
			values["campaigns"] = []
			campaign = {}
			ids = db.distinct_items(cur, table, "campaign_id", "user_id", user_id)
			if ids:
				for id in ids:
					campaign["campaign_name"] = db.get_item(cur, table, "campaign_id", id, "campaign_name")
					campaign["tag_ids"] = db.get_item(cur, table, "campaign_id", id, "tag_ids")
					campaign["create_date"] = db.get_item(cur, table, "campaign_id", id, "create_date")
					campaign["rating"] = db.get_item(cur, table, "campaign_id", id, "rating")
					campaign["review"] = db.get_item(cur, table, "campaign_id", id, "review")
					campaign["reviewer"] = db.get_item(cur, table, "campaign_id", id, "reviewer")
					values["campaigns"].append(campaign)
		if table == "images":
			values["images"] = []
			imgs = {}
			ids = db.distinct_items(cur, table, "img_id", "user_id", user_id)
			if ids:
				for id in ids:
					imgs["img_id"] = id
					imgs["campaign_id"] = db.get_item(cur, table, "img_id", id, "campaign_id")
					imgs["img_url"] = db.get_item(cur, table, "img_id", id, "img_url")
					imgs["img_name"] = db.get_item(cur, table, "img_id", id, "img_name")
					imgs["img_info"] = db.get_item(cur, table, "img_id", id, "img_info")
					values["images"].append(imgs)
		
	elif usertype == "influencer":
		if table == "affiliated_campaigns":
			values["affiliated_campaigns"] = []
			val = db.distinct_items(cur, table, "affil_id", "user_id", user_id)
			if val:
				values["affiliated_campaigns"] = val
				
		if table == "user_favorites":
			values["favorites"] = []
			val = db.distinct_items(cur, table, "favorite_id", "user_id", user_id)
			if val:
				values["favorite_id"] = val
	return values
	
def get_all(con, cur, usertype, user_id):
	"""
	Returns all information of the user.
	args: con (address), cur (address), status (string), user_id(string)
	returns: dictionary
	"""
	if usertype != "admin":
		val = db.get_item(cur, "user_cred", "user_id", user_id, "usertype")
		if val:
			usertype = val
	values = {"success":"1", "reason":"", "user_id":user_id}
	
	tables = gc.get_all_tb(usertype)
	
	for table in tables:
		values = get_values(cur, values, usertype, table, user_id)
		
	if len(values) == 2:
		return {"success":"0", "reason":"user doesn't exists, or information not matched correctly"}
	return values
####################################################################
	
def get_user_info(usertype, user_id, key):
	"""
	Returns a generic get method for either get all or one for user
	args: usertype (string), user_id (string), key (string)
	returns: results (dictionary)
	"""
	remote = False	
	con, cur = gc.setup_db(remote)
	
	# check related tables exist
	if not gc.check_tb_relations(cur, usertype):
		return gc.val_results(con, cur, "0", "NULL", "NULL", "Necessary tables have not yet been created")
	
	if key == "all":
		return get_all(con, cur, usertype, user_id)
	else:
		return get_one(con, cur, usertype, user_id, key)

# print(login("banana@b.", "bananahana"))
# print(get_user_info("user","1", "name"))
# print(get_user_info("influencer","2", "all"))