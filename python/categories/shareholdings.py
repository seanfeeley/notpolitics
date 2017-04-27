# -*- coding: utf-8 -*-
import locale, copy
locale.setlocale( locale.LC_ALL, '' )

import re
from categories import Category
from items import ShareholdingsItem, OtherShareholdingsItem

class Shareholdings(Category):
	def __init__(self):
		"""
		Shareholdings
		"""

		# Init the class, then set some class specific variables
		Category.__init__(self)

		# category info
		self.category_id = 8
		self.category_type = 'shareholdings'
		self.category_description = 'Shareholdings'
		self.isCurrency = False

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
						}

		template['raw'] = raw

		next_num = len(self.entries) + 1
		template['entry_id'] = '%04d' % next_num

		item_id = '%04d' % next_num
		category_id = self.category_id
		raw_string = raw
		pretty = raw
		registered = ''

		# TODO: regex for %, minimum will be 15%
		# find company and value, generate amount
		amount = 1

		self.items.append(ShareholdingsItem(item_id, category_id, raw_string, pretty, registered, amount))


		return template

class OtherShareholdings(Category):
	def __init__(self):
		"""
		Miscellaneous
		"""

		# Init the class, then set some class specific variables
		Category.__init__(self)

		# category info
		self.category_id = 9
		self.category_type = 'shareholdings'
		self.category_description = 'Other Shareholdings'
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
						}

		template['raw'] = raw

		next_num = len(self.entries) + 1
		template['entry_id'] = '%04d' % next_num

		item_id = '%04d' % next_num
		category_id = self.category_id
		raw_string = raw
		pretty = raw
		registered = ''
		amount = 70000

		self.items.append(OtherShareholdingsItem(item_id, category_id, raw_string, pretty, registered, amount))



		return template		