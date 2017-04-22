# -*- coding: utf-8 -*-
import locale

class IntrestType():

	def set(self, raw):
		self.raw.append(raw)
	def parse(self):
		for each in self.raw:
			print '\t%s' % each	

	@property
	def entries(self):
		return len(self.raw)

class Employment(IntrestType):
	def __init__(self):
		"""Employment"""
		self.raw = []

	def parse(self):
		print 'Employment Entries : %s' % len(self.raw)

class IndirectDonations(IntrestType):
	def __init__(self):
		"""IndirectDonations"""
		self.raw = []

class DirectDonations(IntrestType):
	def __init__(self):
		"""DirectDonations"""
		self.raw = []

class GiftsUK(IntrestType):
	def __init__(self):
		"""GiftsUK"""
		self.raw = []

class VisitsNonUK(IntrestType):
	def __init__(self):
		"""VisitsNonUK"""
		self.raw = []

class GiftsNonUK(IntrestType):
	def __init__(self):
		"""GiftsNonUK"""
		self.raw = []

class Shareholdings(IntrestType):
	def __init__(self):
		"""Shareholdings"""
		self.raw = []

	def parse(self):
		print 'Shareholdings Entries : %s' % len(self.raw)

class Miscellaneous(IntrestType):
	def __init__(self):
		"""Miscellaneous"""
		self.raw = []

class Family(IntrestType):
	def __init__(self):
		"""Family"""
		self.raw = []

class Property(IntrestType):
	def __init__(self):
		"""Property"""
		self.raw = []
		self.data = []

	@property
	def hasProperty(self):
		if len(self.raw) > 0:
			return True
		else:
			return False

	@property
	def minimum_owner_value(self):
		value = self.owner * 100000
		locale.setlocale( locale.LC_ALL, '' )
		return locale.currency( value, grouping=True )

	@property
	def minimum_rental_value(self):
		value = self.rental * 10000
		locale.setlocale( locale.LC_ALL, '' )
		return locale.currency( value, grouping=True )

	def summary(self):
		print 'Property - Owner (%s), Rental Income (%s)\n' % (self.minimum_owner_value, self.minimum_rental_value)

	# @property
	def detailed(self):
		for each in self.data:
			print '\t%s' % each['value']

	def parse(self):
		# print 'Parsing Properties'

		self.owner = 0
		self.rental = 0

		for entry in self.raw:

			if '(i)' in entry:
				self.data.append({'value' : entry.split(':')[0], 'type' : 'owner'})
				self.owner += 1

			elif '(ii)' in entry:
				self.data.append({'value' : entry.split(':')[0], 'type' : 'rental'})
				self.rental += 1