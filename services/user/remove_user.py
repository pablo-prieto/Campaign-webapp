import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import base_cmd.db_commands as db
import base_cmd.generic_commands as gc

def remove_user(user_id):
	"""
	Returns a generic remove method
	args: usertype (string), user_id (int)
	returns: dictionary
	"""
	con, cur = gc.setup_db()
	usertype = gc.get_usertype(cur, user_id)
	 
	if db.exist_items(cur, "credentials", user_id = user_id):
		db.del_row(cur, "credentials", "user_id", user_id)
		if usertype != 'admin':
			db.del_row(cur, "profiles", "user_id", int(user_id))
			db.del_row(cur, "configs", "user_id", int(user_id))
			db.del_row(cur, "user_tags", "user_id", int(user_id))
			db.del_row(cur, "user_titles", "user_id", int(user_id))
			db.del_row(cur, "user_queue", "user_id", int(user_id))
			if usertype == "business":
				db.del_row(cur, "businesses", "user_id", int(user_id))
				campaign_ids = db.distinct_items(cur, "campaigns", "campaign_id", "user_id", int(user_id))
				db.del_row(cur, "campaigns", "user_id", int(user_id))
				db.del_row(cur, "images", "user_id", int(user_id))
				if campaign_ids:
					for campaign_id in campaign_ids:
						db.del_row(cur, "campaign_tags", "campaign_id", int(campaign_id))
						db.del_row(cur, "approval_queue", "campaign_id", int(campaign_id))
			elif usertype == "influencer":
				db.del_row(cur, "influencer_platforms", "user_id", int(user_id))
				db.del_row(cur, "affiliated_campaigns", "user_id", int(user_id))
				db.del_row(cur, "user_favorites", "user_id", int(user_id))
		return gc.results(con, cur, "1")
	else:
		return gc.results(con, cur, "0", "user id didn't exist")
			
# print(remove_user(4))