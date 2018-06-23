import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import base_cmd.db_commands as db
import base_cmd.generic_commands as gc

def remove(actor, user_id):
	"""
	Returns a generic remove method
	args: actor (string), user_id (int)
	returns: dictionary
	"""
	remote = False
	con, cur, valid_tables = gc.general_setup(remote, actor)
	
	if actor != "admin" and actor != "user":
		return gc.results(con, cur, "0", "actor given is invalid")
	
	# check if table exists
	if not valid_tables:
		return gc.results(con, cur, "0", "Table has not yet been created")
	
	if actor == "admin":
		if db.exist_items(cur, "admin_cred", user_id = user_id):
			db.del_row(cur, "admin_cred", "user_id", user_id)
			return gc.results(con, cur, "1")
		else:
			return gc.results(con, cur, "0", "user id didn't exist")
	else:
		if db.exist_items(cur, "user_cred", user_id = user_id):
			db.del_row(cur, "user_cred", "user_id", int(user_id))
			db.del_row(cur, "profiles", "user_id", int(user_id))
			db.del_row(cur, "configs", "user_id", int(user_id))
			db.del_row(cur, "user_interests", "user_id", int(user_id))
			db.del_row(cur, "user_favorites", "user_id", int(user_id))
			db.del_row(cur, "user_titles", "user_id", int(user_id))
			db.del_row(cur, "approval_queue", "user_id", int(user_id))
			return gc.results(con, cur, "1")
		else:
			return gc.results(con, cur, "0", "user id didn't exist")
						
#print(remove("user", 3))