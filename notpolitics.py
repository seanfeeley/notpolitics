# -*- coding: utf-8 -*-
import locale, copy
locale.setlocale( locale.LC_ALL, '' )

import ast, os
from bs4 import BeautifulSoup
import operator
from optparse import OptionParser

# local libs
from employment import Employment
from family import FamilyLobbyists, Family
from miscellaneous import Miscellaneous
from land_and_property import Property
from shareholdings import OtherShareholdings, Shareholdings
from gifts import GiftsOutsideUK, Gifts
from visits import VisitsOutsideUK
from donations import DirectDonations, IndirectDonations
from salary import Salary
from utils import get_all_mps, get_request, get_xml_dict, PrettyPrintUnicode

current_xml_files = [os.path.join(os.path.dirname(os.path.abspath(__file__)) , 'data', 'regmem2017-04-10.xml' )]
current_xml_files.append(os.path.join(os.path.dirname(os.path.abspath(__file__)) , 'data', 'regmem2017-03-06.xml' ))

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
		# self.readFromXml()

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

	def readFromXml(self):
		"""Method to read an xml file into a dict"""

		self.category_list_xml = None

		for xml in current_xml_files:

			print xml

			xmldict = get_xml_dict(xml)

			for key in xmldict['regmem']:

				pid = key['personid'].split('/')[-1]

				if pid == self.person_id:


					print '-'*100
					print key['membername']
					print '-'*100

					self.category_list_xml = self.fix_xml_dict(key['category'])
					print ''

					break

	def fix_xml_dict(self, category_list_xml):
		"""Fix up"""

		# create a dictionary of search terms and the corresponding class to initialise when found
		headings = {}
		headings['Employment and earnings'] = Employment() # 1
		headings['Support linked to an MP but received by a local party organisation'] = IndirectDonations() # 2 (a)
		headings['Any other support not included in Category 2(a)'] = DirectDonations() # 2 (b)
		headings['Gifts, benefits and hospitality from UK sources'] = Gifts() # 3
		headings['Visits outside the UK'] = VisitsOutsideUK() # 4
		headings['Gifts and benefits from sources outside the UK'] = GiftsOutsideUK() # 5
		headings['Land and property portfolio'] = Property() # 6
		headings["Shareholdings: over 15% of issued share capital"] = Shareholdings() #7 (i)
		headings["Other shareholdings, valued at more than"] = OtherShareholdings() #7 (ii)
		headings['Miscellaneous'] = Miscellaneous() # 8
		headings['Family members employed and paid from parliamentary expenses'] = Family() # 9
		headings['Family members engaged in lobbying'] = FamilyLobbyists() # 10

		searches = [each for each in headings.keys()]
		import pprint 

		if isinstance(category_list_xml, list):

			new = {}

			for cat in category_list_xml:

				name = cat['name']
				cat_type = cat['type']
				record = cat['record']['item']
				print '-', name, cat_type

				if isinstance(record, str):
					print '\t%s' % record

					for x in searches:
						if x in name:
							new[x] = [record]

				if isinstance(record, list):
					# ok, so i have a list, a list of what?
					for each in record:
						if isinstance(each, str):
							# is a list of strings, lets keep it like that
							for x in searches:
								if x in name:
									new[x] = record
						if isinstance(each, list):
							# ok, so we have list of lists
							pprint.pprint(each)

				# 		if isinstance(each, list):
				# 			for i in each:
				# 				print 'CATEGORY TYPE : LIST/LIST'
				# 				print i, type(i)
				print ''

			print ''
			print 'NEW'
			# import pprint
			# PrettyPrintUnicode.pprint(new)

			return new
		else:
			raise

	def getMPIntrests(self):
		"""Method to parse the full_info variable"""

		intrests = self.full_info['register_member_interests_html']
		soup = BeautifulSoup(intrests, 'html.parser')
		text = soup.text
		splits = text.splitlines()

		# create a dictionary of search terms and the corresponding class to initialise when found
		headings = {}
		headings['Employment and earnings'] = Employment() # 1
		headings['Support linked to an MP but received by a local party organisation'] = IndirectDonations() # 2 (a)
		headings['Any other support not included in Category 2(a)'] = DirectDonations() # 2 (b)
		headings['Gifts, benefits and hospitality from UK sources'] = Gifts() # 3
		headings['Visits outside the UK'] = VisitsOutsideUK() # 4
		headings['Gifts and benefits from sources outside the UK'] = GiftsOutsideUK() # 5
		headings['Land and property portfolio'] = Property() # 6
		headings["Shareholdings: over 15% of issued share capital"] = Shareholdings() #7 (i)
		headings["Other shareholdings, valued at more than"] = OtherShareholdings() #7 (ii)
		headings['Miscellaneous'] = Miscellaneous() # 8
		headings['Family members employed and paid from parliamentary expenses'] = Family() # 9
		headings['Family members engaged in lobbying'] = FamilyLobbyists() # 10

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
		self.salary = Salary(self.office, self.first_name, self.last_name, self.party)

		self.employment = headings['Employment and earnings']
		self.indirect = headings['Support linked to an MP but received by a local party organisation']
		self.direct = headings['Any other support not included in Category 2(a)']
		self.gifts = headings['Gifts, benefits and hospitality from UK sources']
		self.visits_outside_uk = headings['Visits outside the UK'] 
		self.gifts_outside_uk = headings['Gifts and benefits from sources outside the UK'] 
		self.property = headings['Land and property portfolio']
		self.shareholdings = headings["Shareholdings: over 15% of issued share capital"]
		self.other_shareholdings = headings["Other shareholdings, valued at more than"]
		self.miscellaneous = headings['Miscellaneous']
		self.family = headings['Family members employed and paid from parliamentary expenses']
		self.family_lobbyists = headings['Family members engaged in lobbying']

		# append to categories list, iterable
		self.categories.append(self.employment)
		self.categories.append(self.indirect)
		self.categories.append(self.direct)
		self.categories.append(self.gifts)
		self.categories.append(self.visits_outside_uk)
		self.categories.append(self.gifts_outside_uk)
		self.categories.append(self.property)
		self.categories.append(self.shareholdings)
		self.categories.append(self.other_shareholdings)
		self.categories.append(self.miscellaneous)
		self.categories.append(self.family)
		self.categories.append(self.family_lobbyists)
		self.categories.append(self.salary)


	def __str__(self):

		header = '%s\n%s %s (%s, %s) | Declared Annual Income : %s | Declared Wealth : %s\n%s\n' % ('*'*200, self.first_name, self.last_name, self.party, self.constituency, locale.currency(self.income, grouping=True), locale.currency(self.wealth, grouping=True), '*'*200)
		return header

	@property
	def wealth(self):
		value = 0
		for category in self.categories:
			if category.wealth > 0:
				value += category.wealth
		return value

	@property
	def income(self):
		value = 0
		for category in self.categories:
			if category.income > 0:
				value += category.income
		return value

def main(mps, options):

	mps = [MemberOfParliament(member) for member in mps]
	if options.sortby == 'wealth':
		mps = sorted(mps, key=operator.attrgetter('wealth'), reverse=False)
	elif options.sortby == 'income':
		mps = sorted(mps, key=operator.attrgetter('income'), reverse=False)
	else:
		mps = sorted(mps, key=operator.attrgetter('%s.value' % options.sortby), reverse=False)

	for i in mps:
		print i
		categories = sorted(i.categories, key=operator.attrgetter('category_id'), reverse=False)
		opt = False
		for each in categories:
			category = each

			if options.summary:
				opt = True
				print category
			elif options.detailed:
				opt = True
				print category
				for item in category.items:
					print item
				print ''
			elif options.debug:
				opt = True
				print category
				for item in category.items:
					item.pprint()
				print ''
		if opt:
			print ''

if __name__ == "__main__":
	parser = OptionParser()

	parser.add_option("--limit", help="Limit results (pre - sorted)", action="store", type='int', default=650)
	parser.add_option("--summary", help="Summary print", action="store_true", default=False)
	parser.add_option("--detailed", help="Detailed print", action="store_true", default=False)
	parser.add_option("--debug", help="Debug print", action="store_true", default=False)
	parser.add_option("--sortby", help="Sort By", action="store", default='income')

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
				if member.lower() in i['constituency'].lower():
					searched.append(i)

		mps = searched

	if options.limit:
		mps = mps[:options.limit]

	main(mps, options)

