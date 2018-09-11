#!/usr/bin/python
from intercom.client import Client
import intercom.utils
import phue
import time, sys 
import configparser as ConfigParser
import color_conversion as cc
from datetime import datetime, timezone
import json

def log(*args):
	print (time.ctime()),
	for a in args:
		print (str(a)),
	print
	(sys.stdout.flush())

log("starting...")
p = ConfigParser.SafeConfigParser()
p.readfp(open("./light_runner_201808.conf","r"))

log("parsing config...")
config_ip_address = p.get("config","ip")
config_light_number = int(p.get("config", "light_number"))
# config_feedback_url = p.get("config", "feedback_url")
config_username = p.get("config", "username")
# config_website_username = p.get("config", "website_username")
# config_website_password = p.get("config", "website_password")
config_light_count = int(p.get("config", "light_count"))
config_light_number1 = int(p.get("config", "light_number1"))
# automation_url = p.get("config", "automation_url")
intercom_token = p.get("config", "intercom_token")
intercom_app_id = p.get("config", "intercom_app_id")
billing_user = p.get("config", "billing_user")
crossbrowsertesting_user = p.get("config", "crossbrowsertesting_user")
customer_success_user = p.get("config", "customer_success_user")
security_user = p.get("config", "security_user")
technical_success_user = p.get("config", "technical_success_user")
the_crossbrowsertesting_team_user = p.get("config", "the_crossbrowsertesting_team_user")
cbt_team_user = p.get("config", "cbt_team_user")
jl_user = p.get("config", "jl_user")
nb_user = p.get("config", "nb_user")
rl_user = p.get("config", "rl_user")
za_user = p.get("config", "za_user")
sh_user = p.get("config", "sh_user")
dg_user = p.get("config", "dg_user")
jt_user = p.get("config", "jt_user")




log("creating bridge")
bridge = phue.Bridge(ip=config_ip_address, username=config_username)

log("connnect")
bridge.connect()

import requests
from requests.auth import HTTPBasicAuth


# don't need this stuff anymore
# we're going to make a request to intercom instead -- Chase
'''
def get_prod_data():
	r = requests.get(config_feedback_url,
	auth = HTTPBasicAuth(config_website_username, config_website_password))
	return r.text

def get_prod_data2():
	r = requests.get(automation_url,
	auth = HTTPBasicAuth(config_website_username, config_website_password))
	return r.text
'''
DONT_MENTION = [billing_user, crossbrowsertesting_user, customer_success_user, security_user, technical_success_user, the_crossbrowsertesting_team_user, cbt_team_user, jl_user,
	nb_user, rl_user, za_user, sh_user, dg_user]

# Use the intercoms

def get_intercom_data():
	client = Client(personal_access_token=intercom_token)
	opts = {
		'open': True,
		'state': 'open'
	}
	feedback_counter = 0
	conversations= client.conversations.find_all(**opts)
	current_time = datetime.now(timezone.utc)
	user_class = "<class 'intercom.utils.User'>"
	for conversation in conversations:
		if conversation.assignee.id != billing_user and conversation.assignee.id != crossbrowsertesting_user  and conversation.assignee.id != customer_success_user and conversation.assignee.id != security_user and conversation.assignee.id != technical_success_user and conversation.assignee.id != the_crossbrowsertesting_team_user and conversation.assignee.id != cbt_team_user and conversation.assignee.id != jl_user and conversation.assignee.id != nb_user  and conversation.assignee.id!= rl_user  and conversation.assignee.id != za_user and conversation.assignee.id != sh_user and conversation.assignee.id != dg_user and conversation.assignee.id != jt_user:

			full_conversation = client.conversations.find(id=conversation.id)
			parts = sorted(full_conversation.conversation_parts, key=lambda p: p.updated_at)
			if(len(parts) >0):
				last_message = parts[-1]
				diff = current_time - last_message.updated_at
				if(diff.total_seconds() > 1800 and str(type(last_message.author)) == user_class):
					feedback_counter+=1
					print(conversation.id)
			else:
				diff = current_time - full_conversation.created_at
				if(diff.total_seconds() > 1800):
					feedback_counter+=1
					print(conversation.id)


	#oauth_headers = {'Authorization': 'Bearer ' + intercom_token}
#	oauth_headers['Accept'] = 'application/json'
#	feedback_counter = 0
#	current_time = datetime.now(timezone.utc)
	# make a request for all open conversations
#	r = requests.get('https://api.intercom.io/conversations?state=open',headers=oauth_headers)

#	log('status code from request to intercom', r.status_code)
#	if r.status_code == 200:
#		log('JSON response from intercom', 'hello')

	# for each conversation, if the admin_id is feedback, we'll increment
#	for convo in r.json()['conversations']:
		# might not be the best pattern here. The "feedback admin_id"
		# appears to stay constant, but it will be good to check this in the future. 
		#if not Shane, Zach, Nick, Dan, Joan and the waiting since time is less than 4000000000 seconds greater than the created time.
		# "The times are timestamps and a response from an admin makes the last response is from a user more than 30 minutes ago
#		user_class = "<class 'intercom.utils.User'>"

#		if convo['assignee']['id'] != billing_user and convo['assignee']['id'] != crossbrowsertesting_user  and convo['assignee']['id'] != customer_success_user and convo['assignee']['id'] != security_user and convo['assignee']['id'] != technical_success_user and convo['assignee']['id'] != the_crossbrowsertesting_team_user and convo['assignee']['id'] != cbt_team_user and convo['assignee']['id'] != jl_user and convo['assignee']['id'] != nb_user  and convo['assignee']['id']!= rl_user  and convo['assignee']['id'] != za_user and convo['assignee']['id'] != sh_user and convo['assignee']['id'] != dg_user and diff.total_seconds() > 1800 and str(type(last_message.author)) ==user_class:#convo['waiting_since'] < convo['created_at'] + 4000000000:
#			feedback_counter += 1
#			log(convo['id'])
	return feedback_counter

log("getting lights...")
lights = bridge.lights

# print lights[config_light_number].name
# print lights[config_light_number].colormode

# color temp here is 154
# mostly white
WHITE = 154
ORANGE = 500 # this is what I see when I set it like that

# see here for
# where i got these numbers
# http://www.developers.meethue.com/documentation/core-concepts
RED_XY = [0.675,0.322]
BLUE_XY = [0.1691,0.0441]
GOLD_XY = [0.4947,0.472]

# lights[config_light_number].colortemp = 154
# lights[config_light_number].xy = RED_XY


#Just outputting to know the status 
counter = get_intercom_data()
if counter > 0:
	log("switching to red")
	for aLight in lights:
		aLight.xy = RED_XY
	
else:
	log("no feedback, switching to blue")
	for aLight in lights:
		aLight.xy = BLUE_XY
'''

for i in range (1,10):
	log(i, "get prod data - feedback")
	count = get_prod_data()
	log(i, "count from prod data", count)
	try:
		count = int(count)
	except:
		count = 1 #default to a fail


	# check if feedback needs to be shown
	if count > 0:
		# old way
		# light2.rgb(255,0,0)
		log("switching to red")
		lights[config_light_number].xy = RED_XY

		if config_light_count == 2:
			log("light1 changing too")
			lights[config_light_number1].xy = RED_XY

	else:
		log("there was no feedback we need to check automation")

		# this automation count data
		log(i, "get prod data2 - automation")
		count2 = get_prod_data2()
		log(i, "count from prod data2", count2)
		try:
			count2 = int(count2)
		except:
			count2 = 1 #default to a fail
		log(i, "adjusted count automation", count2)

		if count2 > 0:
			log("switching to gold")
			lights[config_light_number].xy = GOLD_XY

			if config_light_count == 2:
				log("light1 changing too")
				lights[config_light_number1].xy = GOLD_XY
		else:
			log("switching to blue")
			lights[config_light_number].xy = BLUE_XY

			if config_light_count == 2:
				log("light1 changing too")
				lights[config_light_number1].xy = BLUE_XY

	time.sleep(5)

"""
	log(i, "get prod data2")
	count = get_prod_data2()
	log(i, "count from prod data2", count)
	try:
		count = int(count)
	except:
		count = 1 #default to a fail
	log(i, "adjusted count", count)

	if count > 0:
		# old way
		# light2.rgb(255,0,0)
		log("switching to gold")
		lights[config_light_number].xy = GOLD_XY

		if config_light_count == 2:
			log("light1 changing too")
			lights[config_light_number1].xy = GOLD_XY

	else:
		log("switching to blue")
		lights[config_light_number].xy = BLUE_XY

		if config_light_count == 2:
			log("light1 changing too")
			lights[config_light_number1].xy = BLUE_XY


	time.sleep(5)

"""

log("fin")

'''