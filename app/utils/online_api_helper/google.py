import googlemaps
from datetime import datetime


class GoogleMap:
    """
    This class helps to conenct to Google Map API.

    https://github.com/googlemaps/google-maps-services-python

    **`Note`**
    -------------

    The reason you don't get the postal code is the query is too broad. If you would add a street name to the query the result will contain a postal code. A solution to your problem if you don't have a street name or don't want to use it is to split the geocoding into two parts:

    Step 1: Use the city to get the GPS coordinates

    https://maps.googleapis.com/maps/api/geocode/json?address=amsterdam

    Step 2: Use the the GPS coordidates to get the postal code

    https://maps.googleapis.com/maps/api/geocode/json?latlng=52.3182742,4.7288558

    """

    __key = 'AIzaSyCdaUMXLJ_iDJvtwwOP10pdHMF0QYMUTYE'
    __client = None

    def __init__(self):
        self.__connect()

    def __connect(self):
        if self.__client == None:
            self.__client = googlemaps.Client(key=self.__key)
        else:
            return

    def geocode_address(self, address):
        """
        Gets the geocode from address.

        :param address: The address (city or country name).

        :return: The geocode (from Google API).
        """
        if self.__client == None:
            self.__connect()
        geocode_res = self.__client.geocode(address)
        return geocode_res

    def get_long_lat(self, address):
        """
        get longtitude-latitude from Google Map API.

        :param address: The address (city or country name).

        :return: The couple of numbers.
        """
        geocode = self.geocode_address(address=address)
        # pprint.pprint(geocode)
        location = geocode[0].get('geometry').get('location')
        long = location['lng']
        lat = location['lat']
        return long, lat

    # print(location)

    def reverse_geocode(self, long, lat):
        """
        Gets name of address from its longtitude-lattitude values.

        :param long: The longitude value.

        :param lat: The lattitude value.

        :return: The name of address.
        """
        if self.__client == None:
            self.__connect()
        reverse_res = self.__client.reverse_geocode((lat, long))
        return reverse_res

    def get_postal_code_by_long_lat(self, lng, lat):
        """
        Get postal code of any address by its longtitude-lattitude values.

        :param long: The longitude value.

        :param lat: The lattitude value.

        :return: The value of the postal code.
        """
        reverse_gecode = self.reverse_geocode(long=lng, lat=lat)
        postal_code = 0
        longname = ''
        shortname = ''
        if isinstance(reverse_gecode, list):
            for i in range(len(reverse_gecode)):
                if postal_code != 0:
                    break
                gecode = reverse_gecode[i]
                if isinstance(gecode, dict):
                    if 'address_components' in gecode:
                        address_components = gecode['address_components']
                        if isinstance(address_components, list):
                            for j in range(len(address_components)):
                                if postal_code != 0:
                                    break
                                address = address_components[j]
                                if isinstance(address, dict):
                                    types = address['types']
                                    if 'postal_code' in types:
                                        longname = address['long_name']
                                        shortname = address['short_name']
                                        postal_code = address['long_name']
        return longname, shortname

    # return reverse_gecode

    def get_name_by_address_postal_code(self, address):
        """
        Gets postal code of address by its postal code.

        :param address: The address.

        :return: The longtitude - lattitude numbers.
        """
        gecode = self.geocode_address(address=address)
        # print(gecode)
        long_name = ''
        short_name = ''
        if isinstance(gecode, list):
            first_gecode = gecode[0]
            if isinstance(first_gecode, dict):
                address_components = first_gecode['address_components']
                if isinstance(address_components, list):
                    for i in range(0, len(address_components)):
                        component = address_components[i]
                        if isinstance(component, dict) and 'postal_code' in component['types']:
                            # print(component['types'])
                            long_name = component['long_name']
                            short_name = component['short_name']
        return long_name, short_name

    def get_address(self, lng, lat):
        """
        Get address from the longtitude and latitude.

        :param lng: Longtitude value

        :param lat: Latitude value

        :return: Street number, Street name, City, Province and Country.
        """
        # khi gui request nhan ve mot danh sach ca dia diem --> can nhan ve dia diem gan nhat

        addresses = self.reverse_geocode(long=lng, lat=lat)
        if addresses is None:
            return None
        if isinstance(addresses, list):
            size_max = min(10, len(addresses))
            min_distance = 10000000
            min_index = 0
            for i in range(0, size_max):
                element = addresses[i]
                if not 'geometry' in element:
                    continue
                geometry = element['geometry']
                if 'location' in geometry:
                    location = geometry['location']
                    lng_i = location['lng']
                    lat_i = location['lat']
                    import math
                    distance = math.sqrt(math.pow((lng - lng_i), 2) + math.pow((lat - lat_i), 2))
                    if min_distance > distance:
                        min_distance = distance
                        min_index = i
            choose_element = addresses[min_index]
            street_number, street, city, province, country = None, None, None, None, None
            if 'address_components' in choose_element:
                address_components = choose_element['address_components']
                if isinstance(address_components, list):
                    for i in range(0, len(address_components)):
                        component = address_components[i]
                        types = component['types']
                        if 'street_number' in types:
                            street_number = component['long_name']
                        if 'route' in types:
                            street = component['long_name']
                        if 'locality' in types or 'political' in types:
                            city = component['long_name']
                        if 'administrative_area_level_1' in types or 'administrative_area_level_2' in types or 'administrative_area_level_3' in types:
                            province = component['long_name']
                        if 'country' in types:
                            country = component['long_name']
            return street_number, street, city, province, country


def get_lnglat(city_name):
    """
    Gets longtitude-lattitude of any city (supported by Google Map)

    :param city_name: The city's name.

    :return: The long-lat values.
    """
    gmaps = GoogleMap()
    long, lat = gmaps.get_long_lat(address=city_name)
    return long, lat


def get_post_code_by_lnglat(lng, lat):
    """
    Gets postal code by long-lat values.

    :param lng: The longtitude value.

    :param lat: The lattitude value.

    :return: The postal code number.

    """
    gmaps = GoogleMap()
    postcode = gmaps.get_postal_code_by_long_lat(lng=lng, lat=lat)
    return postcode


def get_post_code_by_city_name(city_name):
    """
    Get postale code of any city by name.

    :param city_name: The city's name.

    :return: The postal code.
    """
    gmaps = GoogleMap()
    lng, lat = gmaps.get_long_lat(address=city_name)
    lname, shname = gmaps.get_postal_code_by_long_lat(lng=lng, lat=lat)
    return lname


# Testing

import pprint

# pprint.pprint(res)

gmaps = GoogleMap()
city = 'Munich, Germany'
# test get longlat
lng, lat = gmaps.get_long_lat(address=city)
print(lng, lat)
postal_code = gmaps.get_postal_code_by_long_lat(lng=lng, lat=lat)
pprint.pprint(postal_code)

# 11.5819805 48.1351253


# res = gmaps.geocode_address(city)
# lname, sname = gmaps.get_name_by_address_postal_code(address=city)
# print(lname, sname)
# import json
# jtext = json.dumps(res, indent=2)
# address_components = res[0]['address_components']
# if isinstance(address_components, list):
# 	for i in range(0, len(address_components)):
# 		print(address_components[i])
# print(len(address_components))
# print(json.dumps(address_components, indent=2))
# import pprint
# # pprint.pprint(res)
reverse_res = gmaps.reverse_geocode(105.614982, 21.314780)
pprint.pprint(reverse_res)
address = gmaps.get_address(105.614982, 21.314780)
print(address)
