# -*- coding: utf-8 -*-
import requests
import time
import ast
import xml.etree.cElementTree as ElementTree
import locale
locale.setlocale( locale.LC_ALL, '' )
from datetime import datetime

import pprint

class PrettyPrintUnicode(pprint.PrettyPrinter):
    def format(self, object, context, maxlevels, level):
        if isinstance(object, unicode):
            return (object.encode('utf8'), True, False)
        return pprint.PrettyPrinter.format(self, object, context, maxlevels, level)

# Functions
def get_request(url, user=None, headers={}, request_wait_time=3600.00):
	"""Function to return a http get request"""

	if user:
		request = requests.get(url, auth=(user, ''), headers=headers)
	else:
		request = requests.get(url, headers=headers)

	if request.status_code == 201:
		print '*'*100
		print request.status_code
		print ''
		print "Ok, I'll wait for 5 mins"
		time.sleep(request_wait_time)
		return get_request(url, user, headers)
	else:
		return request

def get_all_mps(theyworkyou_apikey):
	"""Function to return a full list of current MPs as """

	url = 'https://www.theyworkforyou.com/api/getMPs?key=%s&output=js' % (theyworkyou_apikey)
	request = get_request(url=url, user=None, headers={})

	# literal eval the json request into actual json
	literal = ast.literal_eval(request.content)

	return literal

def get_xml_dict(xml_file):

	tree = ElementTree.parse(xml_file)
	root = tree.getroot()
	xmldict = XmlDictConfig(root)

	return xmldict

def string_to_datetime(date_string):
    """
    """
    return datetime.strptime(datetime, '%d-%m-%y')

def padded_string(string, padding=190, left=True, right=False):
    """Return a padded string"""
    if left:
        return string.ljust(padding)
    if right:
        return string.rjust(padding)

class XmlListConfig(list):
    def __init__(self, aList):
        for element in aList:
            # print element
            if element:
                # treat like dict
                if len(element) == 1 or element[0].tag != element[1].tag:
                    self.append(XmlDictConfig(element))
                # treat like list
                elif element[0].tag == element[1].tag:
                    self.append(XmlListConfig(element))
            elif element.text:
                text = element.text.strip()
                if text:
                    self.append(text)

class XmlDictConfig(dict):
    def __init__(self, parent_element):
        childrenNames = []
        for child in parent_element.getchildren():
            childrenNames.append(child.tag)

        if parent_element.items(): #attributes
            self.update(dict(parent_element.items()))
        for element in parent_element:
            if element:
                # treat like dict - we assume that if the first two tags
                # in a series are different, then they are all different.
                #print len(element), element[0].tag, element[1].tag
                if len(element) == 1 or element[0].tag != element[1].tag:
                    aDict = XmlDictConfig(element)
                # treat like list - we assume that if the first two tags
                # in a series are the same, then the rest are the same.
                else:
                    # here, we put the list in dictionary; the key is the
                    # tag name the list elements all share in common, and
                    # the value is the list itself
                    aDict = {element[0].tag: XmlListConfig(element)}
                # if the tag has attributes, add those to the dict
                if element.items():
                    aDict.update(dict(element.items()))

                if childrenNames.count(element.tag) > 1:
                    try:
                        currentValue = self[element.tag]
                        currentValue.append(aDict)
                        self.update({element.tag: currentValue})
                    except: #the first of its kind, an empty list must be created
                        self.update({element.tag: [aDict]}) #aDict is written in [], i.e. it will be a list

                else:
                     self.update({element.tag: aDict})
            # this assumes that if you've got an attribute in a tag,
            # you won't be having any text. This may or may not be a
            # good idea -- time will tell. It works for the way we are
            # currently doing XML configuration files...
            elif element.items():
                self.update({element.tag: dict(element.items())})
            # finally, if there are no child tags and no attributes, extract
            # the text
            else:
                self.update({element.tag: element.text})





# xml_data = os.path.dirname(os.path.abspath(__file__)) , 'data')

# current_xml_files = [os.path.join(os.path.dirname(os.path.abspath(__file__)) , 'data', 'regmem2017-04-10.xml' )]
# current_xml_files.append(os.path.join(os.path.dirname(os.path.abspath(__file__)) , 'data', 'regmem2017-03-06.xml' ))




# def readFromXml(self):
#     """Method to read an xml file into a dict"""

#     self.category_list_xml = None

#     for xml in current_xml_files:

#         print xml

#         xmldict = get_xml_dict(xml)

#         for key in xmldict['regmem']:

#             pid = key['personid'].split('/')[-1]

#             if pid == self.person_id:


#                 print '-'*100
#                 print key['membername']
#                 print '-'*100

#                 self.category_list_xml = self.fix_xml_dict(key['category'])
#                 print ''

#                 break

# def fix_xml_dict(self, category_list_xml):
#     """Fix up"""

#     # create a dictionary of search terms and the corresponding class to initialise when found
#     headings = {}
#     headings['Employment and earnings'] = Employment() # 1
#     headings['Support linked to an MP but received by a local party organisation'] = IndirectDonations() # 2 (a)
#     headings['Any other support not included in Category 2(a)'] = DirectDonations() # 2 (b)
#     headings['Gifts, benefits and hospitality from UK sources'] = Gifts() # 3
#     headings['Visits outside the UK'] = VisitsOutsideUK() # 4
#     headings['Gifts and benefits from sources outside the UK'] = GiftsOutsideUK() # 5
#     headings['Land and property portfolio'] = Property() # 6
#     headings["Shareholdings: over 15% of issued share capital"] = Shareholdings() #7 (i)
#     headings["Other shareholdings, valued at more than"] = OtherShareholdings() #7 (ii)
#     headings['Miscellaneous'] = Miscellaneous() # 8
#     headings['Family members employed and paid from parliamentary expenses'] = Family() # 9
#     headings['Family members engaged in lobbying'] = FamilyLobbyists() # 10

#     searches = [each for each in headings.keys()]

#     if isinstance(category_list_xml, list):

#         new = {}

#         for cat in category_list_xml:

#             name = cat['name']
#             cat_type = cat['type']
#             record = cat['record']['item']
#             print '-', name, cat_type

#             if isinstance(record, str):
#                 print '\t%s' % record

#                 for x in searches:
#                     if x in name:
#                         new[x] = [record]

#             if isinstance(record, list):
#                 # ok, so i have a list, a list of what?
#                 for each in record:
#                     if isinstance(each, str):
#                         # is a list of strings, lets keep it like that
#                         for x in searches:
#                             if x in name:
#                                 new[x] = record
#                     if isinstance(each, list):
#                         pass

#         return new
#     else:
#         raise



            






