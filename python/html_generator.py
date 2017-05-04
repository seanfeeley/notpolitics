#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json, os, operator, locale
from optparse import OptionParser
locale.setlocale( locale.LC_ALL, '' )

json_dump_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'json', 'members_dump.json')
images_directory = os.path.join(os.path.dirname(__file__), '..', 'images')

def main(mps, options):
	"""
	Main
	"""
	mps = sort_by_options(mps, options)

	feeback(mps, options)


def feeback(mps, options):
	""""""

	# now print by options specified on commandline
	for member in mps:
		name = member['name']
		income = locale.currency(member['mp_income'], grouping=True)
		wealth = locale.currency(member['mp_wealth'], grouping=True)
		gifts = locale.currency(member['mp_gifts'], grouping=True)
		donations = locale.currency(member['mp_donations'], grouping=True)
		annual = locale.currency(member['mp_annual'], grouping=True)
		forname = member['forname']
		surname = member['surname']
		member_id = member['member_id']

		print '*'*150
		print name, '(' + member['party'] + ')', member['constituency']
		print 'Income :', income, ' |  Wealth :', wealth, ' |  Gifts :', gifts, ' |  Donations :', donations, ' |  Annual :', annual
		print os.path.abspath(os.path.join(images_directory, '%s_%s_%s.png' % (forname, surname, member_id)))
		print '*'*150
		print ''

		for category in member['categories']:

			category_amount = category['category_amount']

			# if its currency, format it
			if category['isCurrency']:
				print '\t', category['category_description'], '', locale.currency(category_amount, grouping=True)
			else:
				print '\t', category['category_description']


			for item in category['items']:

				item_amount = item['amount']

				if category['isCurrency']:
					print '\t\t', item['pretty'], locale.currency(item_amount, grouping=True)
				else:
					print '\t\t', item['pretty']

		print ''

def sort_by_options(mps, options):
	"""
	Sort by options
	"""

	# sort by options specified on commandline
	if options.sortby == 'wealth':
		mps = sorted(mps, key=operator.itemgetter('mp_wealth'), reverse=False)
	
	elif options.sortby == 'income':
		mps = sorted(mps, key=operator.itemgetter('mp_income'), reverse=False)
	
	elif options.sortby == 'gifts':
		mps = sorted(mps, key=operator.itemgetter('mp_gifts'), reverse=False)
	
	elif options.sortby == 'donations':
		mps = sorted(mps, key=operator.itemgetter('mp_donations'), reverse=False)		

	elif options.sortby == 'annual':
		mps = sorted(mps, key=operator.itemgetter('mp_annual'), reverse=False)	

	else:
		mps = sorted(mps, key=operator.itemgetter('%s' % options.sortby), reverse=False)

	return mps

def read_json_file():
	"""
	Read file from json_dump_location
	"""
	with open(json_dump_location) as json_data:
		return json.load(json_data)

if __name__ == "__main__":
	"""
	Commandline run
	"""
	parser = OptionParser()

	# parser.add_option("--summary", help="Summary print", action="store_true", default=True)
	# parser.add_option("--detailed", help="Detailed print", action="store_true", default=False)
	parser.add_option("--sortby", help="Sort By", action="store", default='income')

	# parse the comand line
	(options, args) = parser.parse_args()

	# return a list (of dicts) of mps
	mps = read_json_file()

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

	main(mps, options)
