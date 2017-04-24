# -*- coding: utf-8 -*-
import locale, copy
locale.setlocale( locale.LC_ALL, '' )

import ast
from bs4 import BeautifulSoup
import operator
from optparse import OptionParser

# local libs
from employment import Employment
from salary import Salary
from utils import get_all_mps, get_request

theyworkyou_apikey = 'DLXaKDAYSmeLEBBWfUAmZK3j'
request_wait_time = 3600.0

class MemberOfParliament():
	def __init__(self, member):
		"""Class holding the individual member of parliament"""

		self.categories = []

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

		# create a dictionary of search terms and the corresponding class to initialise when found
		headings = {}
		headings['Employment and earnings'] = Employment()

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
					headings[last_heading].add_entry(i)

		for each in headings.keys():
			headings[each].parse()

		# store dictionary values (classes), as MemberOfParliament class variable
		self.employment = headings['Employment and earnings']
		self.salary = Salary(self.office, self.first_name, self.last_name, self.party)
		
		# append to categories list, iterable
		self.categories.append(self.employment)
		self.categories.append(self.salary)

	def __str__(self):

		header = '\n%s\n%s %s (%s, %s) | Declared Annual Income %s\n%s\n' % ('*'*200, self.first_name, self.last_name, self.party, self.constituency, locale.currency(self.total_income, grouping=True), '*'*200)
		return header

	@property
	def total_income(self):
		income = 0
		for each in self.categories:
			income += each.value
		return income

def main(mps, options):

	mps = [MemberOfParliament(member) for member in mps]
	if options.sortby == 'total':
		mps = sorted(mps, key=operator.attrgetter('total_income'), reverse=False)
	else:
		mps = sorted(mps, key=operator.attrgetter('%s.value' % options.sortby), reverse=False)

	for i in mps:
		print i
		for each in i.categories:
			print each.summary
			if options.detailed:
				each.print_detailed()
				print ''

if __name__ == "__main__":
	parser = OptionParser()

	parser.add_option("--limit", help="Limit results (pre - sorted)", action="store", type='int', default=650)
	parser.add_option("--detailed", help="Detailed print", action="store_true", default=False)
	parser.add_option("--sortby", help="Sort By", action="store", default='total')

	# parse the comand line
	(options, args) = parser.parse_args()

	mps = get_all_mps(theyworkyou_apikey)
	searched = []

	# TODO: fix this crude arg porser
	if args:
		for member in args:
			for i in mps:
				if member.lower() in i['name'].lower():
					searched.append(i)
				if member.lower() in i['party'].lower():
					searched.append(i)					
		mps = searched

	if options.limit:
		mps = mps[:options.limit]

	main(mps, options)

