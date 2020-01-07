from app.modules.common.controller import Controller
from app.app import db
from app.modules.user.user import User
from app.utils.geo import geo_distance
from .passenger import Passenger
from .dto_passenger import DtoPassenger
from datetime import date, time, datetime


class ControllerPassenger(Controller):
    def create(self, data):
        if not isinstance(data, dict):
            return False
        passenger = self._parse_passenger(data=data, passenger=None)
        db.session.add(passenger)
        db.session.commit()
        user_id = passenger.user_id
        user = User.query.filter_by(user_id=user_id).first()
        user.role = 'passenger'
        db.session.commit()
        return passenger

    def get(self):
        passengers = Passenger.query.all()
        return passengers

    def get_by_id(self, object_id):
        passenger = Passenger.query.filter_by(passenger_id=object_id)
        return passenger

    def update(self, object_id, data):
        passenger = Passenger.query.filter_by(passenger_id=object_id)
        if passenger is None:
            return False
        passenger = self._parse_passenger(data=data, passenger=passenger)
        db.session.commit()
        return passenger

    def delete(self, object_id):
        passenger = Passenger.query.filter_by(passenger_id=object_id).first()
        if passenger is None:
            return False
        else:
            user_id = passenger.user_id
            db.session.delete(passenger)
            db.session.commit()
            user = User.query.filter_by(user_id=user_id).first()
            user.role = 'user'
            db.session.commit()
            return True

    def search(self, args):
        if args is None or not isinstance(args, dict):
            return None
        geo_long, geo_lat, country, city, street, max_distance, mode = None, None, None, None, None, None, None
        if 'geo_long' in args:
            geo_long = args['geo_long']
        if 'geo_lat' in args:
            geo_lat = args['geo_lat']
        if 'country' in args:
            country = args['country']
        if 'city' in args:
            city = args['city']
        if 'street' in args:
            street = args['street']
        if 'max_distance' in args:
            max_distance = args['max_distance']
        if 'mode' in args:
            mode = args['mode']

        if geo_long is not None and geo_lat is not None and max_distance is not None:
            passengers = self._get_by_geo(geo_long=geo_long, geo_lat=geo_lat, max_distance=max_distance, mode=mode)
        else:
            passengers = self._get_by_address(country=country, city=city, street=street, max_distance=max_distance)
        return passengers

    # other functions
    def _get_by_geo(self, geo_lat, geo_long, max_distance, mode='km'):
        passengers = Passenger.query.all()
        ret_passengers = list()
        for passenger in passengers:
            distance = geo_distance((passenger.current_geo_long, passenger.current_geo_lat), (geo_long, geo_lat), mode=mode)
            if distance < float(max_distance):
                ret_passengers.append(passenger)
        return ret_passengers

        # passengers = Passenger.query.filter_by(
        #     geo_distance((Passenger.current_geo_long, Passenger.current_geo_lat), (geo_long, geo_lat),
        #                  mode=mode) <= max_distance).all()
        # return passengers

    def _get_by_address(self, country=None, city=None, street=None, max_distance=None):
        query = db.session.query(Passenger)
        users = None
        print("radius=========>",Passenger.radius)
        if country is not None:
            country = '%' + country.strip() + '%'
            query = query.filter(Passenger.current_country.like(country))
        if city is not None:
            city = '%' + city.strip() + '%'
            query = query.filter(Passenger.current_city.like(city))
        if street is not None:
            street = '%' + street.strip() + '%'
            query = query.filter(Passenger.current_street.like(street))
        if max_distance is not None:
            passengers = Passenger.query.all()
            ret_passengers = []
            for passenger in passengers:
                distance = passenger.radius
                if distance < float(max_distance):
                    ret_passengers.append(passenger)
            return ret_passengers
        users = query.all()
        return users

    def _parse_passenger(self, data, passenger=None):
        user_id, current_place, current_country, current_city, current_street, current_geo_long, current_geo_lat, from_place, from_country, from_city, from_street, from_geo_long, from_geo_lat, to_place, to_country, to_city, to_street, to_geo_long, to_geo_lat, go_date, go_time, number_people, radius, chat_available, price_offer = None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None

        user_id = data['user_id']
        # dateTime = datetime.today()
        # print("first=====>",dateTime)
        # print("second=====>",dateTime.isoformat("|"))
        if 'current_place' in data:
            current_place = data['current_place']
        if 'current_country' in data:
            current_country = data['current_country']
        if 'current_city' in data:
            current_city = data['current_city']
        if 'current_street' in data:
            current_street = data['current_street']
        if 'current_geo_long' in data:
            current_geo_long = float(data['current_geo_long'])
        if 'current_geo_lat' in data:
            current_geo_lat = float(data['current_geo_lat'])

        if 'from_place' in data:
            from_place = data['from_place']
        if 'from_country' in data:
            from_country = data['from_country']
        if 'from_city' in data:
            from_city = data['from_city']
        if 'from_street' in data:
            from_street = data['from_street']
        if 'from_geo_long' in data:
            from_geo_long = float(data['from_geo_long'])
        if 'from_geo_lat' in data:
            from_geo_lat = float(data['from_geo_lat'])

        if 'to_place' in data:
            to_place = data['to_place']
        if 'to_country' in data:
            to_country = data['to_country']
        if 'to_city' in data:
            to_city = data['to_city']
        if 'to_street' in data:
            to_street = data['to_street']
        if 'to_geo_long' in data:
            to_geo_long = float(data['to_geo_long'])
        if 'to_geo_lat' in data:
            to_geo_lat = float(data['to_geo_lat'])
        if 'go_date' in data:
            # if isinstance(data['go_date'], date):
            # go_date = date(data['go_date']).isoformat()
            go_date = data['go_date']
        if 'go_time' in data:
            # if isinstance(data['go_time'], time):
            go_time = data['go_time']
            print("time==============", go_time)
        if 'number_people' in data:
            number_people = data['number_people']
        if 'radius' in data:
            radius = data['radius']
        if 'chat_available' in data:
            chat_available = bool(data['chat_available'])
        if 'price_offer' in data:
            price_offer = float(data['price_offer'])

        if passenger is None:
            passenger = Passenger(user_id=user_id, current_place=current_place, current_country=current_country,
                                  current_city=current_city, current_street=current_street,
                                  current_geo_long=current_geo_long, current_geo_lat=current_geo_lat,
                                  from_place=from_place, from_country=from_country, from_city=from_city,
                                  from_street=from_street,
                                  from_geo_long=from_geo_long, from_geo_lat=from_geo_lat, to_place=to_place,
                                  to_country=to_country, to_city=to_city, to_street=to_street, to_geo_long=to_geo_long,
                                  to_geo_lat=to_geo_lat, go_date=go_date, go_time=go_time, number_people=number_people,
                                  radius=radius, chat_available=chat_available, price_offer=price_offer)
        else:
            passenger.user_id = user_id

            passenger.current_place = current_place
            passenger.current_country = current_country
            passenger.current_city = current_city
            passenger.current_street = current_street
            passenger.current_geo_long = current_geo_long
            passenger.current_geo_lat = current_geo_lat

            passenger.from_place = from_place
            passenger.from_country = from_country
            passenger.from_city = from_city
            passenger.from_street = from_street
            passenger.from_geo_long = from_geo_long
            passenger.from_geo_lat = from_geo_lat

            passenger.to_place = to_place
            passenger.to_country = to_country
            passenger.to_city = to_city
            passenger.to_street = to_street
            passenger.to_geo_long = to_geo_long
            passenger.to_geo_lat = to_geo_lat

            passenger.go_date = go_date
            passenger.go_time = go_time

            passenger.number_people = number_people
            passenger.radius = radius
            passenger.chat_available = chat_available
            passenger.price_offer = price_offer
        return passenger
