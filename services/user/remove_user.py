import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import base_cmd.db_commands as db
import base_cmd.generic_commands as gc

def remove_user(usertype, user_id):
	"""
	Returns a generic remove method
	args: usertype (string), user_id (int)
	returns: dictionary
	"""
	remote = False
	con, cur, valid_tables = gc.general_setup(remote, usertype)
	
	if usertype != "admin" and usertype != "user" and usertype != "influencer" and usertype != "business":
		return gc.results(con, cur, "0", "usertype given is invalid")
	
	# check if table exists
	if not valid_tables:
		return gc.results(con, cur, "0", "Table has not yet been created")
	
	if usertype == "admin":
		if db.exist_items(cur, "admin_cred", user_id = user_id):
			db.del_row(cur, "admin_cred", "user_id", user_id)
			return gc.results(con, cur, "1")
		else:
			return gc.results(con, cur, "0", "user id didn't exist")
	elif usertype in ["influencer", "business", "user"]:
		if db.exist_items(cur, "user_cred", user_id = user_id):
			db.del_row(cur, "user_cred", "user_id", int(user_id))
			db.del_row(cur, "profiles", "user_id", int(user_id))
			db.del_row(cur, "configs", "user_id", int(user_id))
			db.del_row(cur, "user_tags", "user_id", int(user_id))
			db.del_row(cur, "user_titles", "user_id", int(user_id))
			db.del_row(cur, "approval_queue", "queued_id", int(user_id))
			if usertype == "business":
				db.del_row(cur, "campaigns", "user_id", int(user_id))
				db.del_row(cur, "images", "user_id", int(user_id))
			elif usertype == "influencer":
				db.del_row(cur, "affiliated_campaigns", "user_id", int(user_id))
				db.del_row(cur, "user_favorites", "user_id", int(user_id))
			return gc.results(con, cur, "1")
		else:
			return gc.results(con, cur, "0", "user id didn't exist")
						
#print(remove("influencer", 2))