import db_commands as db
import generic_commands as gc

def recreate_data(cur):
	"""
	This function will recreate the database and remove any old database.
	args: cur (address)
	returns: none
	"""
	# delete any existing database
	db.del_tb(cur, "admin_cred")	# holds list of admin's name, emails, and passwords
	db.del_tb(cur, "user_cred")	# holds list of company name, name, emails, and passwords
	db.del_tb(cur, "profiles")	# holds list of profiles
	db.del_tb(cur, "configs")
	db.del_tb(cur, "interests")
	db.del_tb(cur, "user_interests")
	db.del_tb(cur, "user_favorites")
	
	db.del_tb(cur, "campaigns")
	db.del_tb(cur, "images")
	db.del_tb(cur, "titles")
	db.del_tb(cur, "user_titles")
	db.del_tb(cur, "approval_queue")
	
	# functions from db_commands
	db.create_tb(cur, "admin_cred", 1, user_id='SERIAL', name='VARCHAR(64)', phone='VARCHAR(12)', email='VARCHAR(64)',
		password='VARCHAR(128)', salt='VARCHAR(32)', reg_date='VARCHAR(10)')
	db.create_tb(cur, "user_cred", 1, user_id='SERIAL', status='VARCHAR(64)', usertype='VARCHAR(16)',
		comp_name='VARCHAR(64)', name='VARCHAR(64)', borough='VARCHAR(16)', state='VARCHAR(16)',
		phone='VARCHAR(12)', email='VARCHAR(64)', password='VARCHAR(128)', salt='VARCHAR(32)', reg_date='VARCHAR(10)')
	db.create_tb(cur, "profiles", 1, user_id='INT', picture_id='VARCHAR(64)', about='VARCHAR(256)')
	db.create_tb(cur, "configs", 1, user_id='INT')
	db.create_tb(cur, "interests", 1, interest_id='SERIAL', interest_name='VARCHAR(32)', info='VARCHAR(256)')
	db.create_tb(cur, "user_interests", 2, user_id='INT', interests='INT')
	# favorite campaigns
	db.create_tb(cur, "user_favorites", 2, user_id='INT', favorites='INT')

	db.create_tb(cur, "campaigns", 1, campaign_id='SERIAL', user_id='INT', campaign_name='VARCHAR(64)',
		tags='VARCHAR(128)', create_date='VARCHAR(10)', rating='INT', review='VARCHAR(256)', reviewer='INT')
	# images for campaign
	db.create_tb(cur, "images", 1, image_id='SERIAL', campaign_id='SERIAL', img_name='VARCHAR(64)', info= 'VARCHAR(128)')
	# earned titles
	db.create_tb(cur, 'titles', 1, title_id='SERIAL', title_name='VARCHAR(32)', info='VARCHAR(128)')
	# titles that are connected to user
	db.create_tb(cur, 'user_titles', 2, user_id='INT', title_id='INT', date='VARCHAR(10)')
	db.create_tb(cur, 'approval_queue', 1, user_id='INT')

# Execution of the functions
if __name__ == "__main__":
	remote = False
	
	print("Creating Database")
	con, cur = gc.setup_db(remote)
	recreate_data(cur)
	gc.close_db(con, cur)
	
	print('Finished successfully.')