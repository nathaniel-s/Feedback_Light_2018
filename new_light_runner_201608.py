#!/usr/bin/python

import phue
import time, datetime, sys
import ConfigParser
import color_conversion as cc

def log(*args):
	print time.ctime(),
	for a in args:
		print str(a),
	print
	sys.stdout.flush()

log("starting...")
#p = ConfigParser.SafeConfigParser()
#p.readfp(open("./new_light_runner_201608.conf","r"))

# log("parsing config...")
# config_ip_address = p.get("config","ip")
# config_light_number = int(p.get("config", "light_number"))
# config_feedback_url = p.get("config", "feedback_url")
# config_username = p.get("config", "username")
# config_website_username = p.get("config", "website_username")
# config_website_password = p.get("config", "website_password")
# config_light_count = int(p.get("config", "light_count"))
# config_light_number1 = int(p.get("config", "light_number1"))
# automation_url = p.get("config", "automation_url")
# intercom_token = p.get("config", "intercom_token")
# feedback_user = p.get("config", "feedback_user")

log("creating bridge")
bridge = phue.Bridge(ip='192.168.192.135', username='mOdAGhvsBmwGUtqDB5akm80Dh7UM78-EyArJeODI')

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

# Use the intercoms
def get_intercom_data():
	oauth_headers = {'Authorization': 'Bearer ' + 'dG9rOjRhOWJmMmQzX2M2NDdfNGZjYV85OTNkXzdiMTIwMDk2ZDNmNDoxOjA='}
	oauth_headers['Accept'] = 'application/json'
	feedback_counter = 0
	# make a request for all open conversations
	r = requests.get('https://api.intercom.io/conversations?state=open',headers=oauth_headers)

	log('status code from request to intercom', r.status_code)
	if r.status_code == 200:
		log('JSON response from intercom', 'hello')

	# for each conversation, if the admin_id is feedback, we'll increment
	for convo in r.json()['conversations']:
		# might not be the best pattern here. The "feedback admin_id"
		# appears to stay constant, but it will be good to check this in the future. 
		#if not Shane, Zach, Nick, Dan, Joan and the waiting since time is less than 4000000000 seconds greater than the created time.
		# "The times are timestamps and a response from an admin makes the waiting since time 2000 years in the future in seconds 40000000000 is 1268 years"
		if convo['assignee']['id'] != '834369' and convo['assignee']['id'] != '1395336' and convo['assignee']['id'] != '1504507'  and convo['assignee']['id'] != '1504507' and convo['assignee']['id'] != '1859972' and convo['assignee']['id'] != '526531' and convo['assignee']['id'] != '1932625' and convo['assignee']['id'] != '1504507' and convo['assignee']['id'] != '1437235'and convo['assignee']['id'] != '17807923771' and convo['assignee']['id'] != '1407570'  and  convo['waiting_since'] < convo['created_at'] + 4000000000:
		#if convo['assignee']['id'] == '1910371' and convo['waiting_since'] < convo['created_at'] + 4000000000:
		#if convo['waiting_since'] < convo['created_at'] + 4000000000:
			feedback_counter += 1
			log(convo['id'])
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

counter = get_intercom_data()
if counter > 0:
	log("switching to red")
	lights[0].xy = RED_XY
else:
	log("no feedback, switching to blue")
	lights[0].xy = BLUE_XY

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