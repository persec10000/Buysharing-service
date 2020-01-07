import json
import requests
from xml.etree import ElementTree
from bs4 import BeautifulSoup
from online_api_helper.google import *
import logging

logger = logging.getLogger(__name__)


class WetterOnline:
	"""
	Connects to Wetter Online to get all information about allergies.

	see more at `"http://api.wetteronline.de/cgi-bin/mkinteractive/mkinteractive?plz="`
	"""
	__plz = ''
	__prefix_link = "http://api.wetteronline.de/cgi-bin/mkinteractive/mkinteractive?plz="
	__link = None

	def __init__(self, plz=None):
		self.__plz = str(plz)
		self.__link = self.__prefix_link + str(self.__plz)

	def set_plz(self, plz):
		self.__plz = plz
		self.__link = self.__prefix_link + self.__plz

	def get_data(self, plz=None):
		"""
		Returns all information about allergies that catched from WetterOnline.

		:param plz: The city's postal code.

		:return: The xml data format.

		"""
		if plz != None:
			self.__plz = str(plz)
			self.__link = self.__prefix_link + self.__plz
		resp = requests.get(self.__link)
		data = resp.text  # json.loads(resp.text)
		# tree = ElementTree.fromstring(resp.text)
		return data


def pollen_message_by_city_name(city_name):
	"""
	Gets pollen message by city name.

	:param city_name: The city's name.

	:return: The message and pollens.

	:return: message: The message in plain-text format.

	:return: pollens: The **`json`** of data from Wetter Online.
	"""
	if city_name == None:
		return ''
	message = ''
	pollens = list()
	try:
		# google = GoogleMap()
		# plz, _ = google.get_name_by_address_postal_code(address=city_name)
		plz = get_post_code_by_city_name(city_name=city_name)
		# print(plz)
		wetter = WetterOnline()
		data = wetter.get_data(plz=plz)
		# message = data
		# print(data)
		soup = BeautifulSoup(data, 'lxml')
		for pollen in soup.findAll('pollen'):
			degree = int(pollen.get('degree'))
			if degree > 0:
				pol = dict()
				pol['kind'] = pollen.get('kind')
				pol['degree'] = pollen.get('degree')
				pol['text'] = pollen.get('text')
				polmess = pollen.get('kind') + "-" + pollen.get('text')
				message += polmess + ';'
				pollens.append(pol)

			# print(pollen.get('degree'), pollen.get('kind'), pollen.get('text'))
	except Exception as e:
		logger.log(e.__repr__())
		# print(getattr(e, 'message', repr(e)))
		message = {'kind': '', 'degree': '', 'text': ''}  # e.__repr__()
	return message, pollens


def pollen_message_by_plz(plz):
	"""
	Gets pollens message by plz.

	:param plz: The plz value.

	:return: The message and pollens.

	:return: message: The message in plain-text format.

	:return: pollens: The **`json`** of data from Wetter Online.
	"""
	if plz == None:
		return None, None
	message = ''
	pollens = list()
	try:
		# google = GoogleMap()
		# plz, _ = google.get_name_by_address_postal_code(address=city_name)
		# print(plz)
		wetter = WetterOnline()
		data = wetter.get_data(plz=plz)
		# message = data
		# print(data)
		soup = BeautifulSoup(data, 'lxml')
		for pollen in soup.findAll('pollen'):
			degree = int(pollen.get('degree'))
			if degree > 0:
				pol = dict()
				pol['kind'] = pollen.get('kind')
				pol['degree'] = pollen.get('degree')
				pol['text'] = pollen.get('text')
				polmess = pollen.get('kind') + "-" + pollen.get('text')
				message += polmess + ';'
				pollens.append(pol)

			# print(pollen.get('degree'), pollen.get('kind'), pollen.get('text'))
	except Exception as e:
		logger.log(e.__repr__())
		# print(getattr(e, 'message', repr(e)))
		message = {'kind': '', 'degree': '', 'text': ''}  # e.__repr__()
	return message, pollens

# message, pollens = pollen_message_by_city_name(city_name='Munich')
# message, pollens = pollen_message_by_plz(plz=80331)
# print(message)
# import pprint
# pprint.pprint(pollens)

# wetter = WetterOnline()
# data = wetter.get_data(plz=53120)
# import pprint
# #pprint.pprint(data)
#
# # tree = ElementTree.fromstring(str(data))
# # root = tree.getroot()
# # for child in root:
# # 	print(child.tag, child.attrib)
#
# soup = BeautifulSoup(data,'lxml')
# for pollen in soup.findAll('pollen'):
# 	print(pollen.get('degree'),pollen.get('kind'), pollen.get('text'))
# 	#pprint.pprint(pollen)
