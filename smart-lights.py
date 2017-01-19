#!/usr/bin/env python
import time
import sys
import requests
import json
from collections import namedtuple

CMD = namedtuple('CMD', 'cmd_name usage')

#CUSTOMIZE THIS
hue = {'ip'       : '{IP_ADDR_OF_YOUR_HUE}',
       'light_map': 	{'light':     ('3', 'Dimmable light'), 
                     	 'nightlamp': ('4', 'Dimmable light')
	         	},
       'username': '{YOUR_APP_ID_HERE}'
       }
#END CUSTOMIZATION

cmd_list = [ CMD('on', "Turns specified light on"),
	     CMD('off', "Turns specified light off"),
	     CMD('get', "Gets the state of specified lamp"),
	     CMD('set', "Sets the attribute=value for specified lamp.\n"
	            	"       Following is the attribute list for different light types\n"
			"       1. Dimmable light:\n"
			"                         brightness=<value>"
			                          "wherevalue is the percentage of max brightness")
           ]	

def usage():
	"""
	Help function
	"""
	print "******\nUsage:\n******"
	print "./smart-lights.py <light_name> <cmd> [cmdarg]\n"
	for cmd in cmd_list:
		print '{:4s} : {:s}'.format(cmd.cmd_name, cmd.usage)
	print "\nSpecify 'all' as light_name to apply cmd to all lights at once"
	print "******\n"

def set_light_state(light_name='nightlamp', cmd='on', cmdarg=None):
	"""
	Usage: set_light_state(<light_name>, <cmd>, <cmdarg>)
		Default light_name is 'nightlamp'
		Default cmd is 'on' which takes no cmdarg
		Other cmds are 'off' (no cmdarg)
		and 'set' (int value representing percentage of full brightness)
	"""
	baseurl = 'http://' + hue['ip'] + '/api/' + hue['username'] + '/'
	url = ''
	body = {"on":True}

	if light_name in hue['light_map'].keys():
		url = baseurl + 'lights/' + hue['light_map'][light_name][0] + '/state'
	elif (light_name == 'all'):
		url = baseurl + 'groups/0/action'
	if (cmd == 'off'):
		body = {"on":False}	
	print json.dumps(body)
	r = requests.put(url, json.dumps(body), timeout=5)
	if r.status_code != 200:
		print r.status_code
	resp = r.json()
	print resp
	print ""

if __name__ == "__main__":
	"""
	Usage: ./smart-lights.py <light_name> <cmd cmdarg>
		Supported values for cmd are on, off, set, get 
	"""
	if (len(sys.argv) == 4):
		set_light_state(sys.argv[1], sys.argv[2], sys.argv[3])
	elif (len(sys.argv) == 3):
		set_light_state(sys.argv[1], sys.argv[2])
	elif (len(sys.argv) == 1):
		usage()
	else:
		set_light_state()
