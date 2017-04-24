# -*- coding: utf-8 -*-
import requests
import time
import ast
import locale
locale.setlocale( locale.LC_ALL, '' )

import pprint

class PrettyPrintUnicode(pprint.PrettyPrinter):
    def format(self, object, context, maxlevels, level):
        if isinstance(object, unicode):
            return (object.encode('utf8'), True, False)
        return pprint.PrettyPrinter.format(self, object, context, maxlevels, level)

# Functions
def get_request(url, user=None, headers={}, request_wait_time=3600.00):
	"""Function to return a http get request"""

	if user:
		request = requests.get(url, auth=(user, ''), headers=headers)
	else:
		request = requests.get(url, headers=headers)

	if request.status_code == 201:
		print '*'*100
		print request.status_code
		print ''
		print "Ok, I'll wait for 5 mins"
		time.sleep(request_wait_time)
		return get_request(url, user, headers)
	else:
		return request

def get_all_mps(theyworkyou_apikey):
	"""Function to return a full list of current MPs as """

	url = 'https://www.theyworkforyou.com/api/getMPs?key=%s&output=js' % (theyworkyou_apikey)
	request = get_request(url=url, user=None, headers={})

	# literal eval the json request into actual json
	literal = ast.literal_eval(request.content)

	return literal