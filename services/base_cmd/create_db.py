import db_commands as db
import generic_commands as gc

def recreate_data(cur):
	"""
	This function will recreate the database and remove any old database.
	args: cur (address)
	returns: none
	"""
	# delete any existing database
	# these are general tables
	db.del_tb(cur, "admin_cred")	# holds list of admin's name, emails, and passwords
	db.del_tb(cur, "user_cred")	# holds list of company name, name, emails, and passwords
	db.del_tb(cur, "profiles")	# holds list of profiles
	db.del_tb(cur, "configs")
	db.del_tb(cur, "user_tags")
	db.del_tb(cur, "user_titles")
	
	# these are tables for influencer
	db.del_tb(cur, "user_favorites")
	db.del_tb(cur, "affiliated_campaigns")
	
	# these are tables for businesses
	db.del_tb(cur, "campaigns")
	db.del_tb(cur, "images")
	
	# collection of items
	db.del_tb(cur, "titles")
	db.del_tb(cur, "tags")
	
	db.del_tb(cur, "approval_queue")
	
	# functions from db_commands
	db.create_tb(cur, "admin_cred", 1, user_id='SERIAL', usertype='VARCHAR(16)', name='VARCHAR(64)', phone='VARCHAR(12)', email='VARCHAR(64)',
		password='VARCHAR(128)', salt='VARCHAR(32)', reg_date='VARCHAR(10)')
	db.create_tb(cur, "user_cred", 1, user_id='SERIAL', status='VARCHAR(64)', usertype='VARCHAR(16)',
		comp_name='VARCHAR(64)', name='VARCHAR(64)', borough='VARCHAR(16)', state='VARCHAR(16)',
		phone='VARCHAR(12)', email='VARCHAR(64)', password='VARCHAR(128)', salt='VARCHAR(32)', reg_date='VARCHAR(10)')
	db.create_tb(cur, "profiles", 1, user_id='INT', picture_id='VARCHAR(64)', about='VARCHAR(256)')
	db.create_tb(cur, "configs", 1, user_id='INT')
	db.create_tb(cur, "user_tags", 2, user_id='INT', tag_id='INT')
	# titles that are connected to user
	db.create_tb(cur, 'user_titles', 2, user_id='INT', title_id='INT', title_date='VARCHAR(10)')
	
	# favorite campaigns
	db.create_tb(cur, "user_favorites", 2, user_id='INT', favorite_id='INT')
	db.create_tb(cur, "affiliated_campaigns", 2, user_id='INT', affil_id='INT')
	
	db.create_tb(cur, "campaigns", 1, campaign_id='SERIAL', user_id='INT', campaign_name='VARCHAR(64)',
		tag_ids='VARCHAR(128)', create_date='VARCHAR(10)', rating='INT', review='VARCHAR(256)', reviewer='INT')
	# images for campaign
	db.create_tb(cur, "images", 1, img_id='SERIAL', user_id='INT', campaign_id='INT', img_url='VARCHAR(64)', img_name='VARCHAR(64)', img_info= 'VARCHAR(128)')
	
	# earned titles
	db.create_tb(cur, 'titles', 1, title_id='SERIAL', title_name='VARCHAR(32)', title_info='VARCHAR(128)')
	db.create_tb(cur, "tags", 1, tag_id='SERIAL', tag_name='VARCHAR(32)', tag_info='VARCHAR(256)')
	
	db.create_tb(cur, 'approval_queue', 1, queued_id='INT')

# Execution of the functions
if __name__ == "__main__":
	remote = False
	
	print("Creating Database")
	con, cur = gc.setup_db(remote)
	recreate_data(cur)
	gc.close_db(con, cur)
	
	print('Finished successfully.')