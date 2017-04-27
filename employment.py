# -*- coding: utf-8 -*-
import locale, copy
locale.setlocale( locale.LC_ALL, '' )

import re
from categories import Category
from items import EmploymentItem

class Employment(Category):
	def __init__(self):
		"""
		Employment
		"""

		# lists of raw entries and parsed entries (dictionaries)
		self.raw_entries = []
		self.entries = []
		self.items = []

		# category info
		self.category_id = 1
		self.category_type = 'employment'
		self.category_description = 'Private Employment'
		self.isCurrency = True

	def do_logic(self, raw):
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
						# 'wealth' : None,
						'hours' : None,
						# 'mins' : None,
						'employer' : None
						}


		# NOTE: usually the register uses 'Hours' to note time taken -  very clunky but works the moment
		# TODO: need to be able to parse hours values into mins, hours, days - basically interpret whatever
		# was filled in on their form.
		# TODO: need to decipher if the amount earned, was donated to party, charity etc
		# TODO: if possible find the employer - could also check companies house to investigate further the links
		# of the employer, other directors, other MPs, relatives etc
		if 'Hours:' in raw:
			registered_regex = re.compile(r"\bRegistered\b \d+ [A-Z][a-z]+ \d+")
			registered_regex = re.compile(r'\((.*?\))')

			hours_regex = re.compile(r"\.")
			amount_regex = re.compile(r"£\d+")

			if hours_regex.search(raw.split('Hours: ')[-1]):
				template['hours'] = raw.split('Hours: ')[-1].split('.')[0]
				hours = raw.split('Hours: ')[-1].split('.')[0]
			else:
				hours = None

			if registered_regex.findall(raw.encode('utf-8'), re.UNICODE):
				x = registered_regex.findall(raw)
				template['registered'] = str(x[-1].replace(')', ''))
				registered = str(x[-1].replace(')', ''))
			else:
				registered = None

			if amount_regex.search(raw.replace(',','').encode('utf-8')):
				template['amount'] = int(amount_regex.search(raw.replace(',', '').encode('utf-8')).group().split('£')[-1])
				amount = int(amount_regex.search(raw.replace(',', '').encode('utf-8')).group().split('£')[-1])
				if 'monthly salary' in raw.lower():
					amount = amount * 12

				if 'a month' in raw.lower():
					amount = amount * 12

			else:
				amount = 0

			template['raw'] = raw
			no_hours = raw.split(' Hours')[0]
			no_reg = no_hours.split('(%s' % template['registered'])[0]
			template['pretty'] = no_reg[:-1]

			next_num = len(self.entries) + 1
			template['entry_id'] = '%04d' % next_num

			item_id = '%04d' % next_num
			category_id = self.category_id
			raw_string = raw
			pretty = no_reg[:-1]

			self.items.append(EmploymentItem(item_id, category_id, raw_string, pretty, registered, amount))

			return template
