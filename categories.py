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
		self.items = []
		
		# category info
		self.category_id = 0
		self.category_type = 'category'
		self.category_description = 'Category Description'
		self.isCurrency = True

	def __str__(self):
		if self.wealth > 0 and self.income > 0:
			return '(%s) %s (Income : %s) (Wealth : %s)' % (self.category_id, self.category_description.encode('utf-8'), locale.currency(self.income, grouping=True), locale.currency(self.wealth, grouping=True))
		elif self.wealth > 0:
			return '(%s) %s (Wealth : %s)' % (self.category_id, self.category_description.encode('utf-8'), locale.currency(self.wealth, grouping=True))
		elif self.income > 0:
			return '(%s) %s (Income : %s)' % (self.category_id, self.category_description.encode('utf-8'), locale.currency(self.income, grouping=True))
		else:
			return '(%s) %s ' % (self.category_id, self.category_description.encode('utf-8'))

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
						'amount' : 0,
						'pretty' : None,
						'raw' : None
						}
		return template

	# @property
	# def value(self):
	# 	"""
	# 	Sums all the amounts in the list of entries
	# 	"""
	# 	value = 0
	# 	for entry in self.entries:
	# 		value += entry['amount']
		
	# 	return value

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

	# @property
	# def hasIncome(self):
	# 	income = False
	# 	for each in self.items:
	# 		if each.isIncome:
	# 			income = True
	# 			break
	# 	return income

	# @property
	# def hasWealth(self):
	# 	wealth = False
	# 	for each in self.items:
	# 		if each.isWealth:
	# 			wealth = True
	# 			break
	# 	return wealth

	@property
	def summary(self):
		"""
		Returns a string summary of all the entries
		"""
		if self.isCurrency:
			return '(%02d) %s - %s' % (len(self.entries), self.category_description, locale.currency(self.value, grouping=True))
		else:
			return '(%02d) %s' % (len(self.entries), self.category_description)

	# @property
	def print_debug(self):
		"""
		Returns a list of entry dictionaries
		"""
		for entry in self.entries:
			PrettyPrintUnicode().pprint(entry)

	# @property
	def print_detailed(self):
		"""
		Returns a list of entry dictionaries
		"""
		for entry in self.entries:
			# if self.isCurrency:
			# 	print '\t%s' % (entry['pretty'], entry['amount'])
			# else:
			print '\t%s' % (entry['pretty'])

	def add_entry(self, raw_data):
		"""
		Adds raw data, in the form of a string to self.entries
		"""
		self.raw_entries.append(raw_data)
		# print 'ADDING (%s) : %s' % (self.category_type, raw_data)
