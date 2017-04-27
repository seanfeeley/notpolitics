# -*- coding: utf-8 -*-
import locale, copy
locale.setlocale( locale.LC_ALL, '' )

import re
from categories import Category
from items import MiscellaneousItem

class Miscellaneous(Category):
	def __init__(self):
		"""
		Miscellaneous
		"""

		# Init the class, then set some class specific variables
		Category.__init__(self)
		
		# category info
		self.category_id = 10
		self.category_type = 'miscellaneous'
		self.category_description = 'Miscellaneous'
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
						'pretty' : None
						}

		registered_regex = re.compile(r"\bRegistered\b \d+ [A-Z][a-z]+ \d+")
		amount_regex = re.compile(r"£\d+")

		if registered_regex.search(raw.encode('utf-8'), re.UNICODE):
			template['registered'] = registered_regex.search(raw.encode('utf-8'), re.UNICODE).group().split('Registered ')[-1]
			registered = registered_regex.search(raw.encode('utf-8'), re.UNICODE).group().split('Registered ')[-1]
		else:
			registered = ''

		if amount_regex.search(raw.replace(',','').encode('utf-8')):
			template['amount'] = int(amount_regex.search(raw.replace(',', '').encode('utf-8')).group().split('£')[-1])
			amount = int(amount_regex.search(raw.replace(',', '').encode('utf-8')).group().split('£')[-1])
		else:
			amount = 0

		template['raw'] = raw.replace('(Registered %s)' % template['registered'], '')

		next_num = len(self.entries) + 1
		template['entry_id'] = '%04d' % next_num

		item_id = '%04d' % next_num
		category_id = self.category_id
		raw_string = raw
		pretty = raw.split(' (Regis')[0]

		self.items.append(MiscellaneousItem(item_id, category_id, raw_string, pretty, registered, amount))

		return template