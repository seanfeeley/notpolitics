# -*- coding: utf-8 -*-
import locale, copy, pprint
locale.setlocale( locale.LC_ALL, '' )

from utils import PrettyPrintUnicode, padded_string

class Category():

	'''
	Class holding a category. Is populated with individual entries, each of the same category type
	'''

	def __init__(self):
		"""Category"""

		# lists of raw entries and parsed entries (dictionaries)
		self.raw_entries = []
		self.entries = []
		self.items = []
		
		# category info
		self.category_id = 0
		self.category_type = 'category'
		self.category_description = 'Category Description'

		# class variables, used for sorting, printing
		self.isCurrency = True
		self.isIncome = False
		self.isWealth = False
		self.isGift = False
		self.isExpense = False

	@property
	def isEmpty(self):
		"""
		Boolean
		"""
		if len(self.raw_entries) == 0:
			return True
		else:
			return False

	def parse(self):
		"""
		Parse the list of raw data strings into entry dictionaries based on self.template
		"""

		for raw in self.raw_entries:
			entry = self.do_logic(raw)
			if entry:
				self.entries.append(entry)

	def do_logic(self, raw):
		"""
		Method performing the logic of parsing raw data into dictionary
		"""

		# placeholder method
		template = {
						'type' : self.category_type,
						'registered' : None,
						'amount' : 0,
						'pretty' : None,
						'raw' : None
						}
		return template

	@property
	def wealth(self):
		"""
		Sums all the amounts in the list of entries
		"""
		value = 0
		for entry in self.items:
			if entry.isWealth:
				value += entry.amount
		
		return value

	@property
	def income(self):
		"""
		Sums all the amounts in the list of entries
		"""
		value = 0
		for entry in self.items:
			if entry.isIncome:
				value += entry.amount
		
		return value

	@property
	def gifts(self):
		"""
		Sums all the amounts in the list of entries
		"""
		value = 0
		for entry in self.items:
			if entry.isGift:
				value += entry.amount
		
		return value

	@property
	def expenses(self):
		"""
		Sums all the amounts in the list of entries
		"""
		value = 0
		for entry in self.items:
			if entry.isExpense:
				value += entry.amount
		
		return value

	def add_entry(self, raw_data):
		"""
		Adds raw data, in the form of a string to self.entries
		"""
		self.raw_entries.append(raw_data)

	def __str__(self):
		description = '(%02d) %s' % (self.category_id, padded_string(self.category_description.encode('utf-8'), 20))

		# if income and wealth (land and property category)
		if self.wealth > 0 and self.income > 0:
			return '%s |  Income : %s  |  Wealth : %s' % (description, locale.currency(self.income, grouping=True), locale.currency(self.wealth, grouping=True))
		
		elif self.wealth > 0:
			return '%s |  Wealth : %s' % (description, locale.currency(self.wealth, grouping=True))
		
		elif self.income > 0:
			return '%s |  Income : %s' % (description, locale.currency(self.income, grouping=True))
		
		elif self.gifts > 0:
			return '%s |  Gifts : %s' % (description, locale.currency(self.gifts, grouping=True))
	
		else:
			return '%s |' % (description)


