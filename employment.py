# -*- coding: utf-8 -*-
import locale, copy
locale.setlocale( locale.LC_ALL, '' )

import re
from categories import Category

class Employment(Category):
	def __init__(self):
		"""
		Employment
		"""

		# lists of raw entries and parsed entries (dictionaries)
		self.raw_entries = []
		self.entries = []

		# category info
		self.category_id = '001'
		self.category_type = 'employment'
		self.category_description = 'Employment and Earnings'
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
						'registered' : None,
						'amount' : 0,
						'days' : None,
						'hours' : None,
						'mins' : None,
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
			mins_regex = re.compile(r"\d+ \bmins\b")
			amount_regex = re.compile(r"£\d+")

			if mins_regex.search(raw.encode('utf-8'), re.UNICODE):
				template['hours'] = mins_regex.search(raw.encode('utf-8'), re.UNICODE).group().split('Hours: ')[-1]

			if registered_regex.search(raw.encode('utf-8'), re.UNICODE):
				template['registered'] = registered_regex.search(raw.encode('utf-8'), re.UNICODE).group().split('Registered ')[-1]
				
			if amount_regex.search(raw.replace(',','').encode('utf-8')):
				template['amount'] = int(amount_regex.search(raw.replace(',', '').encode('utf-8')).group().split('£')[-1])

			template['raw'] = raw

			next_num = len(self.entries) + 1
			template['entry_id'] = '%04d' % next_num
			return template
