import sys
import os
import datetime
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import base_cmd.db_commands as db
import base_cmd.generic_commands as gc

def send_camp_db(cur, status, user_id, campaign_name, style_id, duration, members, create_date, rating, review, reviewer):
	"""
	Will create an account in the database
	args: all strings
	returns: none
	"""
	db.insert_tb(cur, "campaigns", status = gc.quote(status), user_id = user_id, campaign_name=gc.quote(campaign_name),
		style_id = style_id, duration = duration, members = members, create_date=gc.quote(create_date), 
		rating=gc.quote(rating), review=gc.quote(review), reviewer=gc.quote(reviewer))
		
def send_img_db(cur, user_id, campaign_id, img_urls, img_names, img_info):
	for url, img_name, img_info in zip(img_urls, img_names, img_info):
		db.insert_tb(cur, "images", user_id=user_id, campaign_id=campaign_id, img_url=gc.quote(url),
			img_name=gc.quote(img_name), img_info=gc.quote(img_info))
			
def send_camp_tags_db(cur, campaign_id, tag_ids):
	for tag_id in tag_ids:
		db.insert_tb(cur, "campaign_tags", campaign_id = campaign_id, tag_id = tag_id)
		
def setup_campaign(cur, user_id, campaign_name, style_id, tag_ids, duration, img_urls, img_names, img_infos):
	"""
	Will setup appropriate information of the user
	args: all strings
	returns: none
	"""
	status = "INACTIVE"
	members = "0"
	create_date = datetime.datetime.today().strftime('%Y-%m-%d')
	rating = "0"
	review = "NULL"
	reviewer = "0"
	send_camp_db(cur, status, user_id, campaign_name, style_id, duration, members, create_date, rating, review, reviewer)
	
	sql = "SELECT campaign_id FROM campaigns WHERE user_id = '%s' and campaign_name = '%s'" % (user_id, campaign_name)
	cur.execute(sql)
	campaign_id = cur.fetchone()[0]
	
	send_img_db(cur, user_id, campaign_id, img_urls, img_names, img_infos)
	send_camp_tags_db(cur, campaign_id, tag_ids)
	
		
def create_campaign(user_id, campaign_name, style_id, tag_ids, duration, img_urls, img_names, img_infos):
	"""
	The main function for admin creation.
	args: all strings
	returns: results (dictionary)
	"""
	con, cur = gc.setup_db()
	
	duplicate = db.exist_items(cur, 'campaigns', campaign_name = gc.quote(campaign_name))
	if duplicate:
		return gc.results(con, cur, "0", "Campaign already exists")
		
	if db.get_item(cur, "credentials", "user_id", user_id, "usertype") != "business":
		return gc.results(con, cur, "0", "User is not a business owner.")
	
	setup_campaign(cur, user_id, campaign_name, style_id, tag_ids, duration, img_urls, img_names, img_infos)
	return gc.results(con, cur, "1")

	
	
# print(create_campaign(2, "Banana Clubs", [1], ["HTTP"], ["banana"], ["long and yellow"]))