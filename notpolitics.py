import time
import json
import requests
import ast
import pprint
from bs4 import BeautifulSoup
import operator

# local libs
import Intrests

theyworkyou_apikey = 'DLXaKDAYSmeLEBBWfUAmZK3j'
request_wait_time = 3600.0
	
class MemberOfParliament():
	def __init__(self, member):
		"""Class holding the individual member of parliament"""

		# set the member
		self.setMember(member)

		# get more info on the member
		self.getPerson()

		# get full info on mp
		self.getMPInfo()

		# make sense of the html info, regarding registered intrests
		self.getMPIntrests()

	def setMember(self, member):
		"""Set the member variables from the given member dictionary"""

		self.name = member['name']
		self.member_id = member['member_id']
		self.person_id = member['person_id']
		self.party = member['party']
		self.constituency = member['constituency']

		if member.has_key('office'):
			self.office = member['office']
		else:
			self.office = None		

	def getPerson(self):
		"""Method to set more variables"""

		url = 'https://www.theyworkforyou.com/api/getPerson?key=%s&id=%s&output=js' % (theyworkyou_apikey, self.person_id)
		request = get_request(url=url, user=None, headers={})

		# literal eval the json request into actual json
		self.person = ast.literal_eval(request.content)
		self.person = self.person[0]

		self.first_name = self.person['given_name']
		self.last_name = self.person['family_name']

	def getMPInfo(self):
		"""Method queries theyworkforyou again, for the full info on a given member of parliament"""
		
		url = 'https://www.theyworkforyou.com/api/getMPInfo?key=%s&id=%s&output=js' % (theyworkyou_apikey, self.person_id)
		request = get_request(url=url, user=None, headers={})

		# literal eval the json request into actual json
		self.full_info = ast.literal_eval(request.content)

	def getMPIntrests(self):
		"""Method to parse the full_info variable"""

		intrests = self.full_info['register_member_interests_html']
		soup = BeautifulSoup(intrests, 'html.parser')
		text = soup.text
		splits = text.splitlines()

		headings = {}
		headings['Employment and earnings'] = Intrests.Employment()
		headings['Support linked to an MP but received by a local party organisation or indirectly via a central party organisation'] = Intrests.IndirectDonations()
		headings['Any other support not included in Category 2(a)'] = Intrests.DirectDonations()
		headings['Gifts, benefits and hospitality from UK sources'] = Intrests.GiftsUK()
		headings['Visits outside the UK'] = Intrests.VisitsNonUK()
		headings['Gifts and benefits from sources outside the UK'] = Intrests.GiftsNonUK()
		headings['Land and property portfolio'] = Intrests.Property()
		headings["Shareholdings: over 15% of issued share capital"] = Intrests.Shareholdings()
		headings['Miscellaneous'] = Intrests.Miscellaneous()
		headings['Family members employed and paid from parliamentary expenses'] = Intrests.Family()

		last_heading = None
		for i in splits:
			header = False
			for h in headings.keys():
				if h in i:
					header = True
					last_heading = h

			if header:
				pass
			else:
				if last_heading:
					headings[last_heading].set(i)

		self.employment = headings['Employment and earnings']
		self.indirect = headings['Support linked to an MP but received by a local party organisation or indirectly via a central party organisation']
		self.direct = headings['Any other support not included in Category 2(a)']
		self.gifts_uk = headings['Gifts, benefits and hospitality from UK sources']
		self.visist = headings['Visits outside the UK']
		self.gifts_non_uk = headings['Gifts and benefits from sources outside the UK']
		self.property = headings['Land and property portfolio']
		self.shareholdings = headings["Shareholdings: over 15% of issued share capital"]
		self.miscellaneous = headings['Miscellaneous']
		self.family = headings['Family members employed and paid from parliamentary expenses']

	def __str__(self):

		header = '\n%s\n%s %s (%s, %s)\n%s\n' % ('*'*200, self.first_name, self.last_name, self.party, self.constituency, '*'*200)
		# properties = 'Properties : %s\n' % self.property.entries
		# shareholdings = 'Shareholdings : %s\n' % self.shareholdings.entries

		# return '%s%s%s' % (header, properties, shareholdings)
		return header

# Functions
def get_request(url, user=None, headers={}):
	"""Function to return a http get request"""

	if user:
		request = requests.get(url, auth=(user, ''), headers=headers)
	else:
		request = requests.get(url, headers=headers)

	if request.status_code != 200:
		print "Ok, I'll wait for 5 mins"
		time.sleep(request_wait_time)
		return get_request(url, user, headers)
	else:
		return request

def get_all_mps():
	"""Function to return a full list of current MPs as """

	url = 'https://www.theyworkforyou.com/api/getMPs?key=%s&output=js' % (theyworkyou_apikey)
	request = get_request(url=url, user=None, headers={})

	# literal eval the json request into actual json
	literal = ast.literal_eval(request.content)

	return literal

mps = [MemberOfParliament(member) for member in get_all_mps()[:10]]

# sort by surname
mps = sorted(mps, key=operator.attrgetter('last_name'))

for i in mps:
	print i
	if i.property.hasProperty:
		i.property.parse()
		i.property.summary()
		i.property.detailed()

