
import phue
import ConfigParser
import color_conversion as cc

p = ConfigParser.SafeConfigParser()
p.readfp(open("./new_light_runner_201608.conf","r"))

config_ip_address = p.get("config","ip")
config_light_number = int(p.get("config", "light_number"))
config_feedback_url = p.get("config", "feedback_url")
config_username = p.get("config", "username")
config_website_username = p.get("config", "website_username")
config_website_password = p.get("config", "website_password")
config_light_count = int(p.get("config", "light_count"))
config_light_number1 = int(p.get("config", "light_number1"))
automation_url = p.get("config", "automation_url")

b = phue.Bridge(ip=config_ip_address,username=config_username)
b.connect()
print b.get_api()
print "is light 1 on?", b.get_light(1,"on")

print "is light 2 on?", b.get_light(2, "on")

lights = b.lights

RED_XY = [0.675,0.322]
BLUE_XY = [0.1691,0.0441]
GOLD_XY = [0.4947,0.472]

lights[1].xy = cc.rgb_to_xy(230,230,250)
lights[0].xy = GOLD_XY




