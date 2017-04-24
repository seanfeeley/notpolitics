# -*- coding: utf-8 -*-
import locale, copy, pprint
locale.setlocale( locale.LC_ALL, '' )

from utils import PrettyPrintUnicode

class Category():

	'''
	Class holding a category. Is populated with individual entries, each of the same category type
	'''

	def __init__(self):
		"""Category"""

		# lists of raw entries and parsed entries (dictionaries)
		self.raw_entries = []
		self.entries = []
		
		# category info
		self.category_id = '000'
		self.category_type = 'category'
		self.category_description = 'Category Description'
		self.isCurrency = True

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

		# entry template - example template only
		template = {
						'type' : self.category_type,
						'registered' : None,
						'amount' : 0
						}
		return template

	@property
	def value(self):
		"""
		Sums all the amounts in the list of entries
		"""
		value = 0
		for entry in self.entries:
			value += entry['amount']
		
		return value

	@property
	def summary(self):
		"""
		Returns a string summary of all the entries
		"""
		if self.isCurrency:
			return '%s (%s) %s - %s' % (self.category_id, len(self.entries), self.category_description, locale.currency(self.value, grouping=True))
		else:
			return '%s (%s) %s -%s' % (self.category_id, len(self.entries), self.category_description, self.value)

	# @property
	def print_detailed(self):
		"""
		Returns a list of entry dictionaries
		"""
		for entry in self.entries:
			PrettyPrintUnicode().pprint(entry)

	def add_entry(self, raw_data):
		"""
		Adds raw data, in the form of a string to self.entries
		"""
		self.raw_entries.append(raw_data)