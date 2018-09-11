#!/root/tony/python/bin/python

from hue import Hue
import time, datetime,random
import ConfigParser

p = ConfigParser.SafeConfigParser()
p.readfp(open("./light_runner.conf","r"))

config_ip_address = p.get("config","ip_address")
config_light_number = p.get("config", "light_number")
config_feedback_url = p.get("config", "feedback_url")

h = Hue()
h.station_ip = config_ip_address
res = h.get_state()
print res

light2 = h.lights.get(config_light_number)
print "light2", light2

colors = [ (255,0,0), (0,255,0), (0,0,255) ]

while True:
	time.sleep(2)
	p = colors[random.randint(0,2)]
	light2.rgb(p[0],p[1],p[2])




