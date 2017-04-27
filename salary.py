# -*- coding: utf-8 -*-
import locale, copy
locale.setlocale( locale.LC_ALL, '' )

import re, ast, pprint
from categories import Category
from items import SalaryItem, AdditionalSalaryItem
from utils import get_request

governing_parties = ['Conservative']

# TODO: need to thoroughly check these - i may have missed some
# http://researchbriefings.parliament.uk/ResearchBriefing/Summary/CBP-7762
# http://www.parliament.uk/mps-lords-and-offices/government-and-opposition1/her-majestys-government/
salaries = {
			# cabinet and ministers
			'The Prime Minister' : 77570,
			'Secretary of State' : 69552, # Cabinet Minister
			'Parliamentary Under-Secretary' : 23947,
			'Minister' : 33350,
			"The Economic Secretary to the Treasury" : 23947,
			"Exchequer Secretary" : 23947,
			"Chief Secretary to the Treasury" : 33350,
			"The Financial Secretary to the Treasury" : 33350,

			# opposition
			"Leader of Her Majesty's Official Opposition" : 63762,
			'Opposition Chief Whip (Commons)' : 33350,
			'Opposition Deputy Chief Whip' : 19441,

			# whips and speaker
			'Speaker of the House of Commons' : 76564,
			'The Parliamentary Secretary to the Treasury' : 33350, # Chief Whip
			"The Treasurer of Her Majesty's Household" : 33350, # Deputy Chief Whip
			'Assistant Whip (HM Treasury)' : 19441,
			"The Lord Commissioner of Her Majesty's Treasury" : 19441, # Whip
			"The Vice-Chamberlain of Her Majesty's Household" : 19441, 
			"Comptroller (HM Household) (Deputy Chief Whip, House of Commons)" : 19441,

			# other
			"Chairman of Ways and Means" : 41626,
			"First Deputy Chairman of Ways and Means" : 36585,
			"Second Deputy Chairman of Ways and Means" : 36585,
			"The Attorney-General" : 96780,
			"The Solicitor-General" : 59871,
			}

a = {'depts' : [], 'positions' : []}

class Salary(Category):
	def __init__(self, offices, forname, surname, party):
		"""
		Salary
		"""
		self.offices = offices
		self.forname = forname
		self.surname = surname
		self.party = party

		# lists of raw entries and parsed entries (dictionaries)
		self.raw_entries = []
		self.entries = []
		self.items = []

		# category info
		self.category_type = 'salary'
		self.category_id = 13
		self.category_description = 'Public Employment'
		self.isCurrency = True

		# basic salary of on MP, as of April 1st 2016
		self.basic_salary = 74962
		self.panel_of_chairs_salary = 15025
		self.chair_salary = 15025

		self.add_basic_salary()
		self.do_logic(None)

	def add_basic_salary(self):
		"""

		"""

		template = {
						'category_type' : self.category_type,
						'category_id' : self.category_id,
						'entry_id' : None,
						'raw' : 'Basic Salary',
						'pretty' : None,
						'registered' : None,
						'amount' : self.basic_salary,
						}

		next_num = len(self.entries) + 1
		template['entry_id'] = '%04d' % next_num					


		item_id = '%04d' % next_num
		category_id = self.category_id
		raw_string = 'Basic Salary'
		pretty = 'Basic Salary'
		amount = self.basic_salary
		registered = ''

		self.items.append(SalaryItem(item_id, category_id, raw_string, pretty, registered, amount))

		self.entries.append(template)

	def do_logic(self, raw):
		"""
		Method performing the logic of parsing raw data into dictionary
		"""
		if self.offices:
			for office in self.offices:
				dept = office['dept']
				position = office['position']
				pretty = None
				# template = None

				if dept == 'Panel of Chairs':
					amount = self.panel_of_chairs_salary
					pretty = dept
					# template = {
					# 			'category_type' : self.category_type,
					# 			'category_id' : self.category_id,
					# 			'entry_id' : None,
					# 			'raw' : dept,
					# 			'pretty' : None,
					# 			'registered' : None,
					# 			'amount' : self.panel_of_chairs_salary,
					# 			}

				elif 'Committee' in dept and position == 'Chair':
					amount = self.chair_salary
					pretty = dept
					# template = {
					# 			'category_type' : self.category_type,
					# 			'category_id' : self.category_id,
					# 			'entry_id' : None,
					# 			'raw' : dept,
					# 			'pretty' : None,
					# 			'registered' : None,
					# 			'amount' : self.chair_salary,
					# 			}

				for pos in salaries.keys():
					if pos in position:
						if not 'shadow' in position.lower():
							amount = salaries[pos]
							pretty = position
							# template = {
							# 			'category_type' : self.category_type,
							# 			'category_id' : self.category_id,
							# 			'entry_id' : None,
							# 			'raw' : position,
							# 			'pretty' : None,
							# 			'registered' : None,
							# 			'amount' : salaries[pos],
							# 			}				

				if pretty:
					next_num = len(self.entries) + 1
					# template['entry_id'] = '%04d' % next_num


					item_id = '%04d' % next_num
					category_id = self.category_id
					raw_string = pretty
					amount = amount
					registered = ''

					self.items.append(AdditionalSalaryItem(item_id, category_id, raw_string, pretty, registered, amount))



					# self.entries.append(template)
