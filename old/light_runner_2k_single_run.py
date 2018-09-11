#!/root/tony/python/bin/python

from hue import Hue
import time, datetime
import ConfigParser

p = ConfigParser.SafeConfigParser()
p.readfp(open("./light_runner.conf","r"))

config_ip_address = p.get("config","ip_address")
config_light_number = p.get("config", "light_number")
config_feedback_url = p.get("config", "feedback_url")

h = Hue()
h.station_ip = config_ip_address
# TC: 201602??
# the get_state will hang the program if the button is needed to be pressed
# we need a way to timeout this command
# if it has not come back in 15 write a log message and kill the program
res = h.get_state()

light2 = h.lights.get(config_light_number)

import requests
from requests.auth import HTTPBasicAuth

def get_prod_data():
	r = requests.get(config_feedback_url,
	auth=HTTPBasicAuth("cbtadmin", "_w9y8ZdVtF"))
	return r.text

count = get_prod_data()

for i in range (1,10):
	print "Running get_prod_data at :",datetime.datetime.now()
	count = get_prod_data()
	try:
		count = int(count)
	except:
		count = 1 #default to a fail

	if count > 0:
		# light2.rgb(255,255,0)
		# time.sleep(1)
		# light2.alert("lselect");
		light2.rgb(255,0,0)
	else:
		light2.rgb(0,0,255)

	time.sleep(5)


