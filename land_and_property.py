# -*- coding: utf-8 -*-
import locale, copy
locale.setlocale( locale.LC_ALL, '' )

import re
from categories import Category
from items import PropertyItem

class Property(Category):
	def __init__(self):
		"""
		Property
		"""

		# Init the class, then set some class specific variables
		Category.__init__(self)
		
		# category info
		self.category_id = 7
		self.category_type = 'property'
		self.category_description = 'Property'
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
						'entry_type' : None,
						'pretty' : None
						}

		registered_regex = re.compile(r"\bRegistered\b \d+ [A-Z][a-z]+ \d+")


		next_num = len(self.entries) + 1
		template['entry_id'] = '%04d' % next_num
		item_id = '%04d' % next_num
		category_id = self.category_id
		raw_string = raw
		pretty = raw.split(' (Registered')[0]
		
		if registered_regex.search(raw):
			splits = registered_regex.search(raw).group().split('Registered ')
			template['registered'] = splits[-1]
			registered = splits[-1]
		else:
			registered = None

		wealth = False
		income = False
		if '(i)' in raw:
			# print 'FOUND i'
			# template['amount'] = template['amount'] + 100000
			# template['entry_type'] = 'owner'
			template['raw'] = raw.split('(i)')[0]
			amount = template['amount'] + 100000
			i = PropertyItem(item_id, category_id, raw_string, pretty, registered, amount)
			i.isWealth = True
			wealth = True
			# print i.amount

			self.items.append(i)

		if '(ii)' in raw:
			# print 'FOUND ii'
			# template['amount'] = template['amount'] + 10000
			# template['entry_type'] = 'rental'
			template['raw'] = raw.split('(ii)')[0]
			amount = template['amount'] + 10000

			if wealth:
				# print type(next_num)
				nn = next_num + 1
				item_id = '%04d' % nn

			i = PropertyItem(item_id, category_id, raw_string, pretty, registered, amount)
			i.isIncome = True
			# print i.amount

			self.items.append(i)

		return template