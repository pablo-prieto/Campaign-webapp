import db_commands as db
import generic_commands as gc

def recreate_data(cur):
	'''
	This function will recreate the database and remove any old database.
	args: cur (address)
	returns: none
	'''
	# delete any existing database
	# these are general tables
	db.del_tb(cur, 'credentials')
	db.del_tb(cur, 'profiles')	# holds list of profiles
	db.del_tb(cur, 'configs')
	db.del_tb(cur, 'user_tags')
	db.del_tb(cur, 'user_titles')
	
	# these are tables for businesses
	db.del_tb(cur, 'businesses')
	db.del_tb(cur, 'campaigns')
	db.del_tb(cur, 'campaign_tags')
	db.del_tb(cur, 'images')
	db.del_tb(cur, 'approval_queue')
	
	# these are tables for influencer
	db.del_tb(cur, 'influencer_platforms')
	db.del_tb(cur, 'affiliated_campaigns')
	db.del_tb(cur, 'user_favorites')
	
	# collection of items
	db.del_tb(cur, 'titles')
	db.del_tb(cur, 'tags')
	db.del_tb(cur, 'styles')
	db.del_tb(cur, 'platforms')
	
	db.del_tb(cur, 'user_queue')
	
	
	# functions from db_commands
	db.create_tb(cur, 'credentials', 1, user_id='SERIAL', username='VARCHAR(8)', status='VARCHAR(16)', usertype='VARCHAR(16)',
		first_name='VARCHAR(16)', last_name='VARCHAR(16)', borough='VARCHAR(16)', state='VARCHAR(16)',
		phone='VARCHAR(12)', email='VARCHAR(32)', password='VARCHAR(128)', salt='VARCHAR(32)', create_date='VARCHAR(10)')
	db.create_tb(cur, 'profiles', 1, user_id='INT', pic_url='VARCHAR(64)', active_tag_id='INT', about='VARCHAR(256)')
	db.create_tb(cur, 'configs', 1, user_id='INT')
	db.create_tb(cur, 'user_tags', 2, user_id='INT', tag_id='INT')
	# titles that are connected to user
	db.create_tb(cur, 'user_titles', 2, user_id='INT', title_id='INT', create_date='VARCHAR(10)')
	
	# these are tables for businesses
	db.create_tb(cur, 'businesses', 1, business_id='SERIAL', user_id='INT', name='VARCHAR(16)', address='VARCHAR(64)', tag_id='INT')
	db.create_tb(cur, 'campaigns', 1, campaign_id='SERIAL', status='VARCHAR(16)', user_id='INT', campaign_name='VARCHAR(64)',
		style_id='INT', duration='INT', members='INT', create_date='VARCHAR(10)', rating='INT', review='VARCHAR(256)', reviewer='INT')
	# images for campaign
	db.create_tb(cur, 'images', 1, img_id='SERIAL', user_id='INT', campaign_id='INT', img_url='VARCHAR(64)', img_name='VARCHAR(64)', img_info= 'VARCHAR(128)')
	db.create_tb(cur, 'campaign_tags', 2, campaign_id='INT', tag_id='INT')
	db.create_tb(cur, 'approval_queue', 2, campaign_id='INT', user_id='INT', create_date='VARCHAR(10)')
	
	# these are tables for influencer
	db.create_tb(cur, 'influencer_platforms', 2, user_id='INT', platform_id='INT', link='VARCHAR(64)')
	db.create_tb(cur, 'affiliated_campaigns', 2, user_id='INT', campaign_id='INT', status='VARCHAR(16)', create_date='VARCHAR(10)')
	db.create_tb(cur, 'user_favorites', 2, user_id='INT', favorite_id='INT')
	
	# earned titles
	db.create_tb(cur, 'titles', 1, title_id='SERIAL', title_name='VARCHAR(32)', title_info='VARCHAR(128)')
	db.create_tb(cur, 'tags', 1, tag_id='SERIAL', tag_name='VARCHAR(32)', tag_info='VARCHAR(256)')
	db.create_tb(cur, 'styles', 1, style_id='SERIAL', style_name='VARCHAR(16)', style_info='VARCHAR(64)')
	db.create_tb(cur, 'platforms', 2, user_id='INT', platform_id='INT')
	
	db.create_tb(cur, 'user_queue', 1, user_id='INT', create_date='VARCHAR(10)')

# Execution of the functions
if __name__ == '__main__':
	print('Creating Database')
	con, cur = gc.setup_db()
	recreate_data(cur)
	gc.close_db(con, cur)
	
	print('Finished successfully.')