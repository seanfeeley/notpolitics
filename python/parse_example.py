import json, os
from utils import PrettyPrintUnicode

json_dump_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'json', 'members_dump.json')

with open(json_dump_location) as json_data:
    d = json.load(json_data)
    # PrettyPrintUnicode().pprint(d)
    # print(d)

for member in d:
	name = member['name']
	print '*'*150
	print '%s (%s)  Income : %s  |  Wealth : %s  |  Gifts : %s  |  Donations : %s  |  Total Annual : %s' % (name, member['party'], member['mp_income'], member['mp_wealth'], member['mp_gifts'], member['mp_donations'], member['mp_annual'])
	print '*'*150
	print ''
	# print member.keys()
	
	# print member['mp_income']
	# print member['mp_wealth']
	# print member['mp_gifts']
	# print member['mp_donations']


	for category in member['categories']:

		# if category['category_type'] == ''

		print '\t%s (%s)' % (category['category_description'], len(category['items']))

		# print category['category_income']
		# print category['category_wealth']
		# print category['category_gifts']
		# print category['category_donations']

		if len(category['items']) > 0:

			for item in category['items']:

				print '\t\t%s (%s)' % (item['pretty'], item['amount'])

		# 		# for key in item.keys():
		# 		# 	print '\t\t%s : %s' % (key, item[key])
		# 		# print ''
		# print ''

	print ''

print len(d)


if __name__ == "__main__":
	parser = OptionParser()

	# parser.add_option("--limit", help="Limit results (pre - sorted)", action="store", type='int', default=650)
	# parser.add_option("--summary", help="Summary print", action="store_true", default=False)
	# parser.add_option("--detailed", help="Detailed print", action="store_true", default=False)
	# parser.add_option("--debug", help="Debug print", action="store_true", default=False)
	# parser.add_option("--sortby", help="Sort By", action="store", default='income')
	# parser.add_option("--from", help="From Date", action="store", default='lastest')
	parser.add_option("--json", help="Dump to Json file", action="store_true", default=True)

	# parse the comand line
	(options, args) = parser.parse_args()

	# return a list (of dicts) of mps
	mps = get_all_mps(theyworkyou_apikey)
	# mps = get_xml_dict(xml_data_file)

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

	# if options.limit:
	# 	mps = mps[:options.limit]

	main(mps, options)






# def sort_by_options(options, mps):
# 	"""
# 	Sort by options
# 	"""

# 	# sort by options specified on commandline
# 	if options.sortby == 'wealth':
# 		mps = sorted(mps, key=operator.attrgetter('total_wealth'), reverse=False)
	
# 	elif options.sortby == 'income':
# 		mps = sorted(mps, key=operator.attrgetter('total_income'), reverse=False)
	
# 	elif options.sortby == 'gifts':
# 		mps = sorted(mps, key=operator.attrgetter('total_gifts'), reverse=False)
	
# 	elif options.sortby == 'expenses':
# 		mps = sorted(mps, key=operator.attrgetter('total_expenses'), reverse=False)		

# 	elif options.sortby == 'annual':
# 		mps = sorted(mps, key=operator.attrgetter('total_annual'), reverse=False)	

# 	else:
# 		mps = sorted(mps, key=operator.attrgetter('%s.value' % options.sortby), reverse=False)

# 	return mps

# def feeback(options, mps):
# 	""""""

# 	# now print by options specified on commandline
# 	for mp in mps:
# 		# the mp class is formatted, to print total income, wealth, gifts and expenses
# 		# plus the mp name, party and constituency
# 		print mp

# 		# sort the categories by their id value
# 		categories = sorted(mp.categories, key=operator.attrgetter('category_id'), reverse=False)
		
# 		opt = False
# 		for category in categories:

# 			if options.summary:
# 				opt = True

# 				# the category class is formatted to print it's name and total value - a summary
# 				print category

# 			elif options.detailed:
# 				opt = True
# 				print category

# 				for item in category.items:
# 					# the item class is formatted to hopefully print a useful bit of data
# 					# needs improvement
# 					print item

# 				print ''
# 		if opt:
# 			print ''

# 	return mps		