# -*- coding: utf-8 -*-
import locale, copy
locale.setlocale( locale.LC_ALL, '' )

import re
from categories import Category
from items import FamilyItem, FamilyLobbyistsItem

class FamilyLobbyists(Category):
	def __init__(self):
		"""
		Family Lobbyists
		"""

		# lists of raw entries and parsed entries (dictionaries)
		self.raw_entries = []
		self.entries = []
		self.items = []

		# category info
		self.category_id = 12
		self.category_type = 'family_lobbyists'
		self.category_description = 'Family Lobbyists'
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
						'registered' : None,
						'amount' : 0,
						'pretty' : None
						}

		template['raw'] = raw

		next_num = len(self.entries) + 1
		template['entry_id'] = '%04d' % next_num

		item_id = '%04d' % next_num
		category_id = self.category_id
		raw_string = raw
		pretty = raw.split(' (Regis')[0]
		amount = 0
		registered = ''

		self.items.append(FamilyLobbyistsItem(item_id, category_id, raw_string, pretty, registered, amount))


		return template

class Family(Category):
	def __init__(self):
		"""
		Family
		"""

		# lists of raw entries and parsed entries (dictionaries)
		self.raw_entries = []
		self.entries = []
		self.items = []

		# category info
		self.category_id = 11
		self.category_type = 'family'
		self.category_description = 'Family'
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
						'registered' : None,
						'amount' : 0,
						'pretty' : None
						}

		template['raw'] = raw

		next_num = len(self.entries) + 1
		template['entry_id'] = '%04d' % next_num

		item_id = '%04d' % next_num
		category_id = self.category_id
		raw_string = raw
		pretty = raw.split(' (Regis')[0]
		amount = 0
		registered = ''

		self.items.append(FamilyItem(item_id, category_id, raw_string, pretty, registered, amount))


		return template