import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import base_cmd.db_commands as db
import base_cmd.generic_commands as gc

def login(username, password):
	"""
	Returns user id given the username and password
	"""
	con, cur = gc.setup_db()
	table = 'credentials'
	
	if "@" in username:
		input_type = "email"
	else:
		input_type = "phone"
	hashpassword = gc.hash_login_pass(cur, table, input_type, username, password)
	
	cur.execute("SELECT user_id, usertype FROM %s WHERE %s = '%s' and password = '%s'" % (table, input_type, username, hashpassword))
	value = cur.fetchone()
	
	if value: # else we know that a user was able to login
		# check if user's account has been activated by admin
		if db.get_item(cur, table, 'user_id', value[0], 'status') == "inactive":
			return gc.val_results(con, cur, "0", value[0], value[1], "User's information has yet to be confirmed")
		return gc.val_results(con, cur, "1", value[0], value[1])
	
	# else if still does not exist, there is no such credentials
	return gc.val_results(con, cur, "0", "NULL", "NULL", "Wrong username and/or password")
	
##################################################################################################	
def get_one(con, cur, usertype, user_id, key):
	"""
	Returns selected information of the user.
	args: con (address), cur (address), usertype (string), user_id(string), key (string)
	returns: dictionary
	"""
	# find out table which table we want
	table = gc.find_table(cur, "user", user_id, key)
	if not table:
		return gc.val_results(con, cur, "0", "NULL", "NULL", "no such key")
	
	value = db.get_item(cur, table, 'user_id', user_id, key)

	if not value:
		value = "NULL"
	return gc.val_results(con, cur, "1", value, usertype)
	
###########################################
	
def get_values(cur, values, usertype, table, user_id):
	"""
	Returns a value and the correct usertype (admin or user) of the user.
	args: cur (address), usertype (string), user_id(string)
	returns: value (any), usertype (string)
	"""
	if usertype == "admin":
		if table == "credentials":
			values["status"] = db.get_item(cur, table, "user_id", user_id, "status")
			values["first_name"] = db.get_item(cur, table, "user_id", user_id, "first_name")
			values["last_name"] = db.get_item(cur, table, "user_id", user_id, "last_name")
			values["borough"] = db.get_item(cur, table, "user_id", user_id, "borough")
			values["state"] = db.get_item(cur, table, "user_id", user_id, "state")
			values["phone"] = db.get_item(cur, table, "user_id", user_id, "phone")
			values["email"] = db.get_item(cur, table, "user_id", user_id, "email")
			values["create_date"] = db.get_item(cur, table, "user_id", user_id, "create_date")
		elif table == "user_queue":
			values["queued_id"] = []
			val = db.distinct_items(cur, table, "user_id")
			if val:
				values["queued_id"] = val
		else:
			pass
	elif usertype == "business" or usertype == "influencer":
		if table == "credentials":
			values["status"] = db.get_item(cur, table, "user_id", user_id, "status")
			values["first_name"] = db.get_item(cur, table, "user_id", user_id, "first_name")
			values["last_name"] = db.get_item(cur, table, "user_id", user_id, "last_name")
			values["borough"] = db.get_item(cur, table, "user_id", user_id, "borough")
			values["state"] = db.get_item(cur, table, "user_id", user_id, "state")
			values["phone"] = db.get_item(cur, table, "user_id", user_id, "phone")
			values["email"] = db.get_item(cur, table, "user_id", user_id, "email")
			values["create_date"] = db.get_item(cur, table, "user_id", user_id, "create_date")
		elif table == "profiles":
			values["pic_url"] = db.get_item(cur, table, "user_id", user_id, "pic_url")
			values["about"] = db.get_item(cur, table, "user_id", user_id, "about")
			values["active_tag_id"] = db.get_item(cur, table, "user_id", user_id, "active_tag_id")
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
		else:
			pass
	if usertype == "business":
		if table == 'businesses':
			values["businesses"] = []
			business = {}
			ids = db.distinct_items(cur, table, "business_id", "user_id", user_id)
			if ids:
				for id in ids:
					business["business_id"] = id
					business["name"] = db.get_item(cur, table, "business_id", id, "name")
					business["address"] = db.get_item(cur, table, "business_id", id, "address")
					business["tag_id"] = db.get_item(cur, table, "business_id", id, "tag_id")
					values["businesses"].append(business)
		elif table == "campaigns":
			values["campaigns"] = []
			campaign = {}
			approval_queue = {}
			ids = db.distinct_items(cur, table, "campaign_id", "user_id", user_id)
			if ids:
				for id in ids:
					campaign["campaign_id"] = id
					campaign["status"] = db.get_item(cur, table, "campaign_id", id, "status")
					campaign["campaign_name"] = db.get_item(cur, table, "campaign_id", id, "campaign_name")
					campaign["duration"] = db.get_item(cur, table, "campaign_id", id, "duration")
					campaign["members"] = db.get_item(cur, table, "campaign_id", id, "members")
					campaign["create_date"] = db.get_item(cur, table, "campaign_id", id, "create_date")
					campaign["rating"] = db.get_item(cur, table, "campaign_id", id, "rating")
					campaign["review"] = db.get_item(cur, table, "campaign_id", id, "review")
					campaign["reviewer"] = db.get_item(cur, table, "campaign_id", id, "reviewer")
					campaign["campaign_tags"] = db.get_item(cur, table, "campaign_id", id, "reviewer")
					
					style_id = db.get_item(cur, table, "campaign_id", id, "style_id")
					campaign["style_name"] = db.get_item(cur, "styles", "style_id", style_id, "style_name")
					
					campaign["campaign_tags"] = db.distinct_items(cur, "campaign_tags", "tag_id", "campaign_id", id)
					campaign["approval_queue"] = db.distinct_items(cur, "approval_queue", "user_id", "campaign_id", id)
					
					values["campaigns"].append(campaign)
					
		elif table == "images":
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
		elif table == "approval_queue":
			values["approval_queue"] = []
			approval_queue = {}
			ids = db.distinct_items(cur, table, "campaign_id", "user_id", user_id)
			if ids:
				for id in ids:
					approval_queue["campaign_id"] = id
					approval_queue["user_ids"] = db.distinct_items(cur, "approval_queue", "user_id", "campaign_id", id)
					values["approval_queue"].append(approval_queue)
		
	elif usertype == "influencer":
		if table == "influencer_platforms":
			values["influencer_platforms"] = []
			influencer_platforms = {}
			ids = db.distinct_items(cur, table, "platform_id", "user_id", user_id)
			if ids:
				for id in ids:
					influencer_platforms["platform_id"] = id
					
					cur.execute("SELECT link FROM platforms WHERE user_id = %s AND platform_id = %s" % (user_id, id))
					link = cur.fetchone()
					if link:
						influencer_platforms["link"] = link[0]
						
					values["influencer_platforms"].append(influencer_platforms)
					
		if table == "affiliated_campaigns":
			values["affiliated_campaigns"] = []
			affiliated_campaigns = {}
			ids = db.distinct_items(cur, table, "campaign_id", "user_id", user_id)
			if ids:
				for id in ids:
					affiliated_campaigns["campaign_id"] = id
					
					cur.execute("SELECT status FROM affiliated_campaigns WHERE user_id = %s AND campaign_id = %s" % (user_id, id))
					status = cur.fetchone()
					if status:
						affiliated_campaigns["status"] = status[0]
						
					values["affiliated_campaigns"].append(affiliated_campaigns)
				
		elif table == "user_favorites":
			values["favorite_id"] = []
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
	# this is the base of our dictionary
	values = {"user_id":user_id, "usertype":usertype}
	
	tables = gc.get_all_tb(usertype)
	
	for table in tables:
		values = get_values(cur, values, usertype, table, user_id)

	if len(values) == 2:
		return gc.val_results(con, cur, "0", "NULL", "NULL", "user doesn't exists, or information not matched correctly")
	return gc.val_results(con, cur, "1", values, usertype)
####################################################################
	
def get_user_info(user_id, key):
	"""
	Returns a generic get method for either get all or one for user
	args: usertype (string), user_id (string), key (string)
	returns: results (dictionary)
	"""
	con, cur = gc.setup_db()
	usertype = gc.get_usertype(cur, user_id)
	
	if key == "all":
		return get_all(con, cur, usertype, user_id)
	else:
		return get_one(con, cur, usertype, user_id, key)

# print(login("banana@b.", "bananahana"))
# print(get_user_info("4", "first_name"))
# print(get_user_info("14", "all"))