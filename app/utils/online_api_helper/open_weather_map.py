import pyowm


class OWMConnection():
	"""
	This class connects to Open Weather Map and get data (using pywom to interact with).
	"""
	__owm_api_key = '54c53b2c82717a11d927717b7000aadc'

	def __init__(self, city=None, lang=None):
		"""
		The constructor.

		:param city: The city.

		:param lang: The language.
		"""
		self.city = city
		self.owm = pyowm.OWM(self.__owm_api_key, language=lang)

	def get_weather(self, city=None):
		"""
		Returns the weather of the specified city.

		:param city: The name of city.

		:return: the weather in the json format.

		"""
		self.city = city
		observation = self.owm.weather_at_place(self.city)
		w = observation.get_weather()
		return w

	def get_wind(self, city=None):
		"""
		Gets wind of the weather of the specified city.

		:param city: The name of city.

		:return: The wind of the city.
		"""
		wind = self.get_weather(city=city).get_wind()
		return wind

	def get_humidity(self, city=None):
		"""
		Gets the humidity of the specified city.

		:param city: The name of city.

		:return: The hummidity.
		"""
		humidity = self.get_weather(city=city).get_humidity()
		return humidity

	def get_temperature(self, city=None, unit=None):
		"""
		Gets temperature of any city by name and return in format of unit given (C or F)

		:param city: The city's name.

		:param unit: The unit of temperature (C or F).

		:return: The temperature of the city.
		"""
		temperature = self.get_weather(city=city).get_temperature(unit=unit)
		return temperature

# import json
# weather = Weather(lang='de')
# w = weather.get_weather(city='Munich')
# print(w.__dict__)
# wind = w.get_wind()
# print(wind)
# humidity = w.get_humidity()
# print(humidity)
# temp = w.get_temperature(unit='celsius')
# print(temp)