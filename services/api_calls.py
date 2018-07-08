# DESCRIPTION: This program will generate possible data if given an endpoint.
import sys
import os
import user.create_user as create_user
import user.update_user as update_user
import user.get_user_info as get_user_info
import user.remove_user as remove_user

import campaign.create_campaign as create_campaign
import requests
import datetime
import time
from flask import Flask, jsonify, request
time_compiled = datetime.datetime.now()

app = Flask(__name__)

"""
Possible API calls are found in api_list.txt
"""

@app.errorhandler(404)
def page_not_found(error):
	return ('page_not_found.html', 404)

	
# test_run: https://
@app.route('/')
def flask_creation():
	"""
	Getting date of when it was last modified
	args: none
	returns: message of compilation (string)
	"""
	return ("API UP AND RUNNING, LAST COMPILED AT: {}".format(str(time_compiled)), 200)

# test_run: Make sure you remove next lines delimiters
""" 
curl http://localhost:3000/user/create-user -d "{\"usertype\": \"influencer\", 
"\"comp_name\": \"banana\", "\"name\": \"banana\", \"borough\":\"Manhattan\", \"state\": \"NY\", 
"\"phone\":\"718-239-4738\", \"email\":\"banana@b.\", \"password\":\"bananahana\"}" -H "Content-Type: application/json"
"""
@app.route('/user/create-user', methods=['POST'])
def create_new_user():
	"""
	This function creates a new user
	"""
	input = request.get_json()
	return (jsonify(create_user.create_user(input["usertype"], input["comp_name"], input["name"],
		input["borough"], input["state"], input["phone"], input["email"], input["password"])), 200)
		
@app.route('/user/create-admin', methods=['POST'])
def create_new_admin():
	"""
	This function creates a new user
	"""
	input = request.get_json()
	return (jsonify(create_user.create_admin(input["usertype"], input["name"], input["phone"], input["email"], input["password"])), 200)
		
@app.route('/user/approve-user', methods=['PUT'])
def approve():
	"""
	This function creates a new user
	"""
	input = request.get_json()
	return (jsonify(update_user.approve_user(input["user_id"], input["status"])), 200)
	
# test_run: curl http://localhost:3000/user/login -d "{\"username\": \"banana@b.\", \"password\": \"bananahana\"}" -H "Content-Type: application/json"
@app.route('/user/login', methods=['POST'])
def login():
	"""
	This function logs in
	"""
	input = request.get_json()
	return (jsonify(get_user_info.login(input["username"], input["password"])), 200)

# test_run: curl http://localhost:3000/user/update -X PUT -d "{\"usertype\": \"admin\", \"user_id\": \"1\", \"key\": \"name\", \"value\": \"Mr.Banana\"}" -H "Content-Type: application/json"
@app.route('/user/update-user', methods=['PUT'])
def make_update():
	"""
	This function will update user
	"""
	input = request.get_json()
	return (jsonify(update_user.update_user(input["usertype"], input["user_id"], input["key"], input["value"])), 200)
	
# test_run: curl http://localhost:3000/user/get-info -d "{\"usertype\": \"admin\", \"user_id\": \"1\", \"key\": \"name\"}"  -H "Content-Type: application/json"
# or
# curl http://localhost:3000/user/get-info -d "{\"usertype\": \"admin\", \"user_id\": \"1\", \"key\": \"all\"}" -H "Content-Type: application/json"
@app.route('/user/get-info', methods=['POST'])
def grab_user_info():
	"""
	This function will get information from a user
	"""
	input = request.get_json()
	return (jsonify(get_user_info.get_user_info(input["usertype"], input["user_id"], input["key"])), 200)
	
# test_run: curl http://localhost:3000/user/remove -d "{\"usertype\": \"admin\", \"user_id\": \"1\"}" -H "Content-Type: application/json"
@app.route('/user/remove', methods=['DELETE'])
def delete_user():
	"""
	This will remove a user
	"""
	input = request.get_json()
	return (jsonify(remove_user.remove_user(input["usertype"], input["user_id"])), 200)


################################################################################################################################################################################
# test_run: curl http://localhost:3000/user/remove -d "{\"user_id\": \"1\", \"campaign_name\": \"Banana club\", \"tags\": \"club\", \"img_urls\": \"HTTP\", \"img_names\": \"Banana club\", \"img_infos\": \"Banana club\"}" -H "Content-Type: application/json"
@app.route('/campaign/create-campaign', methods=['POST'])
def make_campaign():
	"""
	This will remove a user
	"""
	input = request.get_json()
	return (jsonify(create_campaign.create_campaign(input["user_id"], input["campaign_name"], input["tag_ids"], input["img_urls"], input["img_names"], input["img_infos"])), 200)

if __name__ == "__main__":
	app.run(host='localhost', port=3000)