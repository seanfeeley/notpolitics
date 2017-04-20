import csv, ast
import os, pprint
import requests

companies_house_user = 'ZCCtuxpY7uvkDyxLUz37dCYFIgke9PKfhMlEGC-Q'

def get_companies_house_users(member):
	"""Get data from companies house"""

	# id
	member_id = member['@Member_Id']

	# names
	first_name = member['BasicDetails']['GivenForename'].lower()
	last_name = member['BasicDetails']['GivenSurname'].lower()
	names = [first_name, last_name]
	
	# party / constituency
	party = member['Party']['#text']
	constituency = member['MemberFrom']

	# ADDRESSES
	# get all the addresses
	addresses = member['Addresses']['Address']
	physical_addresses = []
	for i in addresses:
		if i['IsPhysical'] == 'True':
			address = {}

			for k in i.keys():
				# x = x.lower().replace(',','')
				if i[k]:
					if k.startswith('Address'):
						for x in i[k].split(' '):
							x = x.lower().replace(',','')
							if x not in physical_addresses:
								physical_addresses.append(x)
					if k == 'Postcode':
						physical_addresses.append(i[k])
						for x in i[k].split(' '):
							x = x.lower().replace(',','')
							if x not in physical_addresses:
								physical_addresses.append(x)

	# NAMES
	# get all the names
	basic_details = member['BasicDetails']

	if member['BasicDetails']['GivenMiddleNames']:
		middle_name = member['BasicDetails']['GivenMiddleNames'].lower()
		names.append(member['BasicDetails']['GivenMiddleNames'].lower())

	if member['ListAs']:
		for x in member['ListAs'].split(' '):
			x = x.lower().replace(',','')
			if x not in names:
				names.append(x)

	if member['FullTitle']:
		for x in member['FullTitle'].split(' '):
			x = x.lower().replace(',','')
			if x not in names:
				names.append(x)

	if member['DisplayAs']:
		for x in member['DisplayAs'].split(' '):
			x = x.lower().replace(',','')
			if x not in names:
				names.append(x)

	preferred_names = member['PreferredNames']['PreferredName']
	if type(preferred_names) == dict:
		preferred_names = [preferred_names]
	
	for i in preferred_names:

		if i['AddressAs']:
			for x in i['AddressAs'].split(' '):
				x = x.lower().replace(',','')
				if x not in names:
					names.append(x)

		if i['Forename']:
			for x in i['Forename'].split(' '):
				x = x.lower().replace(',','')
				if x not in names:
					names.append(x)

		if i['HonouraryPrefixes']:
			for x in i['HonouraryPrefixes']['HonouraryPrefix']['Name'].split(' '):
				x = x.lower().replace(',','')
				if x not in names:
					names.append(x)

		if i['MiddleNames']:
			for x in i['MiddleNames'].split(' '):
				x = x.lower().replace(',','')
				if x not in names:
					names.append(x)

		if i['Surname']:
			for x in i['Surname'].split(' '):
				x = x.lower().replace(',','')
				if x not in names:
					names.append(x)

		if i['Title']:
			for x in i['Title'].split(' '):
				x = x.lower().replace(',','')
				if x not in names:
					names.append(x)

		if i['Suffix']:
			for x in i['Suffix'].split(' '):
				x = x.lower().replace(',','')
				if x not in names:
					names.append(x)

	remove = ['mp', 'mr', 'mrs', 'miss', 'ms']
	for i in names:
		if i in remove:
			names.remove(i)

	# get the date of birth
	dob = member['DateOfBirth']

	print '\n\n\n'
	print '*'*100
	print first_name, last_name, party, constituency
	print '*'*100

	url = 'https://api.companieshouse.gov.uk/search/officers?q=%s+%s&items_per_page=100' % (first_name, last_name)
	# url = 'https://api.companieshouse.gov.uk/search/officers?q=%s&items_per_page=100' % ('+'.join(names))
	# url = 'https://api.companieshouse.gov.uk/search/officers?q=%s+%s&items_per_page=100' % ('+'.join(names), '+'.join(physical_addresses))

	# print url
	r = requests.get(url, auth=(companies_house_user, ''))
	data = r.json()

	data = filter_by_first_last_name(data, first_name, last_name)
	data = filter_by_appointment_counts(data)

	return data

def filter_by_first_last_name(data, first_name, last_name):

	matched_people = []

	for i in data['items']:

		if first_name in i['title'].lower():
			if last_name in i['title'].lower():
				matched_people.append(i)

	return matched_people

def filter_by_appointment_counts(data, count=0):

	matched_people = []

	for i in data:

		if i['appointment_count'] > count:
			matched_people.append(i)

	return matched_people

def get_appointments(mem, user):

	# pprint.pprint(user)

	link = user['links']['self']
	title = user['title']
	address = user['address']
	address_snippet = user['address_snippet']

	officer_id = link.split('/')[2]

	print ''
	print title, address_snippet

	url = 'https://api.companieshouse.gov.uk/officers/%s/appointments' % officer_id
	appointments = requests.get(url, auth=(companies_house_user, ''))
	try:
		appointments = appointments.json()

		# pprint.pprint(appointments)

		for app in appointments['items']:
			role = app['officer_role']
			company_links = app['links']
			company_name = app['appointed_to']['company_name']
			company_number = app['appointed_to']['company_number']
			company_status = app['appointed_to']['company_status']
			# appointed_on = app['appointed_on']
			
			if app.has_key('resigned_on'):
				resigned_on = app['resigned_on']
			if app.has_key('occupation'):
				occ = app['occupation']

			print '\t%s, %s, %s' % (company_name, company_status, role)
	except:
		print '\tdecode error'

def get_house_of_commons_members():

	# http://data.parliament.uk/membersdataplatform/memberquery.aspx#outputs
	search_criteria = 'House=Commons|IsEligible=true'
	outputs = 'BasicDetails|Addresses|PreferredNames'
	url = 'http://data.parliament.uk/membersdataplatform/services/mnis/members/query/%s/%s' % (search_criteria, outputs)
	
	headers = {'Accept': 'application/json'}
	req = requests.get(url, headers=headers)

	# replace null with None
	content = req.content.replace("null", "None")
	a = ast.literal_eval(content)
	members = a['Members']['Member']

	return members

def main():

	members = get_house_of_commons_members()

	for mem in members:
		users = get_companies_house_users(mem)

		for user in users:
			appointments = get_appointments(mem, user)


if __name__ == "__main__":
    main()
