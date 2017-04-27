# -*- coding: utf-8 -*-
import locale, copy
locale.setlocale( locale.LC_ALL, '' )

import re
from categories import Category
from items import GiftsItem

class Gifts(Category):
	def __init__(self):
		"""
		Gifts
		"""

		# lists of raw entries and parsed entries (dictionaries)
		self.raw_entries = []
		self.entries = []
		self.items = []

		# category info
		self.category_id = 4
		self.category_type = 'gifts'
		self.category_description = 'Gifts'
		self.isCurrency = True

	def do_logic(self, raw):
		"""
		Method performing the logic of parsing raw data into dictionary
		"""
		# print raw
		template = {
						'category_type' : self.category_type,
						'category_id' : self.category_id,
						'entry_id' : None,
						'raw' : None,
						'pretty' : None,
						'registered' : None,
						'amount' : 0,
						'donor' : None,
						'address' : None,
						'date_received' : None,
						'date_accepted' : None,
						'donor_status' : None,
						'purpose' : None
						}


		# headings = []
		# headings.append('Name of donor: ')
		# headings.append('Address of donor: ')
		# headings.append('Amount of donation or nature and value if donation in kind: ')
		# headings.append('Date received: ')
		# headings.append('Date accepted: ')
		# headings.append('Donor status: ')
		# headings.append('(Registered ')


		catch = []
		catch.append(['Name of donor: ', 'Address of donor: '])
		catch.append(['Address of donor: ', 'Amount of donation or nature and value if donation in kind: '])
		catch.append(['Amount of donation or nature and value if donation in kind: ', 'Date accepted: '])
		catch.append(['Amount of donation or nature and value if donation in kind: ', 'Date received: '])
		catch.append(['Date received: ', 'Date accepted: '])
		catch.append(['Date accepted: ', 'Donor status: '])
		catch.append(['Donor status: ', r'\(Registered '])


		registered_regex = re.compile(r"\bRegistered\b \d+ [A-Z][a-z]+ \d+")
		if registered_regex.search(raw.encode('utf-8'), re.UNICODE):
			template['registered'] = registered_regex.search(raw.encode('utf-8'), re.UNICODE).group().split('Registered ')[-1]
			registered = registered_regex.search(raw.encode('utf-8'), re.UNICODE).group().split('Registered ')[-1]
		else:
			registered = None
		# catch.append([r'\(Registered ', ''])

		amount_regex = re.compile(r"£\d+")
		# amount_regex = re.compile(r"£\d+")

		search_string = raw
		purpose = raw
		amount = 0
		for k in catch:
			# print 'CATCH : %s' % k

			reg = r'%s(.*?)%s' % (k[0], k[1])
			r = re.search(r'%s(.*?)%s' % (k[0], k[1]), raw)
			# print r
			if r:
				r = r.group(1)
				# print r
				if 'Name of donor' in k[0]:
					template['donor'] = r
				if 'Address of donor' in k[0]:
					template['address'] = r
				if 'Amount of donation' in k[0]:

					if amount_regex.search(r.replace(',','').encode('utf-8')):
						amount = int(amount_regex.search(r.replace(',', '').encode('utf-8')).group().split('£')[-1])
						# print amount.group()
						template['amount'] = int(amount_regex.search(r.replace(',', '').encode('utf-8')).group().split('£')[-1])
						template['purpose'] = r
						purpose = r


				if 'Date received' in k[0]:
					template['date_received'] = r

				if 'Date accepted: ' in k[0]:
					template['date_accepted'] = r

				if 'Donor status: ' in k[0]:
					template['donor_status'] = r
			# else:
			# 	purpose = ''

				# if '(Registered ' in k[0]:
				# 	template['registered'] = r

		template['raw'] = raw
		template['raw'] = 'Donor : %s\n\tAddress : %s\n\tAmount : %s\n\tDonor Status : %s\n\tPurpose : %s' % (template['donor'], template['address'], template['amount'], template['donor_status'], template['purpose'])

		next_num = len(self.entries) + 1
		template['entry_id'] = '%04d' % next_num


		item_id = '%04d' % next_num
		category_id = self.category_id
		raw_string = raw
		pretty = purpose

		self.items.append(GiftsItem(item_id, category_id, raw_string, pretty, registered, amount))

		return template

class GiftsOutsideUK(Category):
	def __init__(self):
		"""
		Gifts from outside the UK
		"""

		# lists of raw entries and parsed entries (dictionaries)
		self.raw_entries = []
		self.entries = []
		self.items = []

		# category info
		self.category_id = 6
		self.category_type = 'gifts_outside_uk'
		self.category_description = 'Gifts Outside UK'
		self.isCurrency = True


	def do_logic2(self, raw):
		"""
		Method performing the logic of parsing raw data into dictionary
		"""

		template = {
						'category_type' : self.category_type,
						'category_id' : self.category_id,
						'entry_id' : None,
						'raw' : None,
						'pretty' : None,
						'registered' : None,
						'amount' : 0,
						'donor' : None,
						'address' : None,
						'date_received' : None,
						'date_accepted' : None,
						'donor_status' : None,
						'purpose' : None
						}


		headings = []
		headings.append('Name of donor: ')
		headings.append('Address of donor: ')
		headings.append('Amount of donation or nature and value if donation in kind: ')
		headings.append('Date received: ')
		headings.append('Date accepted: ')
		headings.append('Donor status: ')
		headings.append('(Registered ')


		catch = []
		catch.append(['Name of donor: ', 'Address of donor: '])
		catch.append(['Address of donor: ', 'Amount of donation or nature and value if donation in kind: '])
		catch.append(['Amount of donation or nature and value if donation in kind: ', 'Date received: '])
		catch.append(['Date received: ', 'Date accepted: '])
		catch.append(['Date accepted: ', 'Donor status: '])
		catch.append(['Donor status: ', r'\(Registered '])


		registered_regex = re.compile(r"\bRegistered\b \d+ [A-Z][a-z]+ \d+")
		if registered_regex.search(raw.encode('utf-8'), re.UNICODE):
			template['registered'] = registered_regex.search(raw.encode('utf-8'), re.UNICODE).group().split('Registered ')[-1]
		# catch.append([r'\(Registered ', ''])

		amount_regex = re.compile(r"£\d+")
		# amount_regex = re.compile(r"£\d+")

		search_string = raw
		for k in catch:
			# print 'CATCH : %s' % k

			reg = r'%s(.*?)%s' % (k[0], k[1])
			r = re.search(r'%s(.*?)%s' % (k[0], k[1]), raw)
			if r:
				r = r.group(1)
				if 'Name of donor' in k[0]:
					template['donor'] = r
				if 'Address of donor' in k[0]:
					template['address'] = r
				if 'Amount of donation' in k[0]:

					if amount_regex.search(r.replace(',','').encode('utf-8')):
						amount = amount_regex.search(r.encode('utf-8'))
						# print amount.group()
						template['amount'] = int(amount_regex.search(r.replace(',', '').encode('utf-8')).group().split('£')[-1])
						template['purpose'] = r


				if 'Date received' in k[0]:
					template['date_received'] = r

				if 'Date accepted: ' in k[0]:
					template['date_accepted'] = r

				if 'Donor status: ' in k[0]:
					template['donor_status'] = r

				# if '(Registered ' in k[0]:
				# 	template['registered'] = r

		template['raw'] = raw
		template['raw'] = 'Donor : %s\n\tAddress : %s\n\tAmount : %s\n\tDonor Status : %s\n\tPurpose : %s' % (template['donor'], template['address'], template['amount'], template['donor_status'], template['purpose'])

		next_num = len(self.entries) + 1
		template['entry_id'] = '%04d' % next_num
		return template


	def do_logic(self, raw):
		"""
		Method performing the logic of parsing raw data into dictionary
		"""
		# print raw
		template = {
						'category_type' : self.category_type,
						'category_id' : self.category_id,
						'entry_id' : None,
						'raw' : None,
						'pretty' : None,
						'registered' : None,
						'amount' : 0,
						'donor' : None,
						'address' : None,
						'date_received' : None,
						'date_accepted' : None,
						'donor_status' : None,
						'purpose' : None
						}


		# headings = []
		# headings.append('Name of donor: ')
		# headings.append('Address of donor: ')
		# headings.append('Amount of donation or nature and value if donation in kind: ')
		# headings.append('Date received: ')
		# headings.append('Date accepted: ')
		# headings.append('Donor status: ')
		# headings.append('(Registered ')


		catch = []
		catch.append(['Name of donor: ', 'Address of donor: '])
		catch.append(['Address of donor: ', 'Amount of donation or nature and value if donation in kind: '])
		catch.append(['Amount of donation or nature and value if donation in kind: ', 'Date accepted: '])
		catch.append(['Amount of donation or nature and value if donation in kind: ', 'Date received: '])
		catch.append(['Date received: ', 'Date accepted: '])
		catch.append(['Date accepted: ', 'Donor status: '])
		catch.append(['Donor status: ', r'\(Registered '])


		registered_regex = re.compile(r"\bRegistered\b \d+ [A-Z][a-z]+ \d+")
		if registered_regex.search(raw.encode('utf-8'), re.UNICODE):
			template['registered'] = registered_regex.search(raw.encode('utf-8'), re.UNICODE).group().split('Registered ')[-1]
			registered = registered_regex.search(raw.encode('utf-8'), re.UNICODE).group().split('Registered ')[-1]
		else:
			registered = None
		# catch.append([r'\(Registered ', ''])

		amount_regex = re.compile(r"£\d+")
		# amount_regex = re.compile(r"£\d+")

		search_string = raw
		purpose = raw
		amount = 0
		for k in catch:
			# print 'CATCH : %s' % k

			reg = r'%s(.*?)%s' % (k[0], k[1])
			r = re.search(r'%s(.*?)%s' % (k[0], k[1]), raw)
			# print r
			if r:
				r = r.group(1)
				# print r
				if 'Name of donor' in k[0]:
					template['donor'] = r
				if 'Address of donor' in k[0]:
					template['address'] = r
				if 'Amount of donation' in k[0]:

					if amount_regex.search(r.replace(',','').encode('utf-8')):
						amount = int(amount_regex.search(r.replace(',', '').encode('utf-8')).group().split('£')[-1])
						# print amount.group()
						template['amount'] = int(amount_regex.search(r.replace(',', '').encode('utf-8')).group().split('£')[-1])
						template['purpose'] = r
						purpose = r


				if 'Date received' in k[0]:
					template['date_received'] = r

				if 'Date accepted: ' in k[0]:
					template['date_accepted'] = r

				if 'Donor status: ' in k[0]:
					template['donor_status'] = r
			# else:
			# 	purpose = ''

				# if '(Registered ' in k[0]:
				# 	template['registered'] = r

		template['raw'] = raw
		template['raw'] = 'Donor : %s\n\tAddress : %s\n\tAmount : %s\n\tDonor Status : %s\n\tPurpose : %s' % (template['donor'], template['address'], template['amount'], template['donor_status'], template['purpose'])

		next_num = len(self.entries) + 1
		template['entry_id'] = '%04d' % next_num


		item_id = '%04d' % next_num
		category_id = self.category_id
		raw_string = raw
		pretty = purpose

		self.items.append(GiftsItem(item_id, category_id, raw_string, pretty, registered, amount))

		return template		
