from app.modules.common.controller import Controller
from app.app import db
from app.modules.user.user import User
from app.utils.geo import geo_distance
from .driver import Driver
from .dto_driver import DtoDriver
from datetime import date, time


class ControllerDriver(Controller):
    def create(self, data):
        driver = self._parse_driver(data=data, driver=None)
        db.session.add(driver)
        db.session.commit()
        user_id = driver.user_id
        user = User.query.filter_by(user_id=user_id).first()
        user.role = 'driver'
        db.session.commit()
        return driver

    def get(self):
        drivers = Driver.query.all()
        return drivers

    def get_by_id(self, object_id):
        driver = Driver.query.filter_by(driver_id=object_id).first()
        return driver

    def update(self, object_id, data):
        driver = Driver.query.filter_by(driver_id=object_id).first()
        if driver is None:
            return False
        driver.car_model = data['car_model']
        driver.car_color = data['car_color']
        driver.car_plate = data['car_plate']
        driver.price_offer = data['price_offer']
        db.session.commit()
        return driver

    def delete(self, object_id):
        driver = Driver.query.filter_by(driver_id=object_id).first()
        if driver is None:
            return False
        else:
            user_id = driver.user_id
            db.session.delete(driver)
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
            buyers = self._get_by_geo(geo_long=geo_long, geo_lat=geo_lat, max_distance=max_distance, mode=mode)
        else:
            buyers = self._get_by_address(country=country, city=city, street=street, max_distance=max_distance)
        return buyers

    # other functions
    def _get_by_geo(self, geo_lat, geo_long, max_distance, mode='km'):
        drivers = Driver.query.all()
        ret_drivers = list()
        for driver in drivers:
            distance = geo_distance((driver.current_geo_long, driver.current_geo_lat), (geo_long, geo_lat), mode=mode)
            if distance < float(max_distance):
                ret_drivers.append(driver)
        return ret_drivers

        # users = Driver.query.filter_by(
        #     geo_distance((Driver.current_geo_long, Driver.current_geo_lat), (geo_long, geo_lat),
        #                  mode=mode) <= max_distance).all()
        # return users

    def _get_by_address(self, country=None, city=None, street=None, max_distance=None):
        query = db.session.query(Driver)
        users = None
        if country is not None:
            country = '%' + country.strip() + '%'
            query = query.filter(Driver.current_country.like(country))
        if city is not None:
            city = '%' + city.strip() + '%'
            query = query.filter(Driver.current_city.like(city))
        if street is not None:
            street = '%' + street.strip() + '%'
            query = query.filter(Driver.current_street.like(street))
        if max_distance is not None:
            query = query.filter(Driver.radius<max_distance)
        users = query.all()
        return users


    def _parse_driver(self, data, driver=None):
        user_id, current_place, current_country, current_city, current_street, current_geo_long, current_geo_lat, target_place, target_country, target_city, target_street, target_geo_long, target_geo_lat, go_date, go_time, arrive_date, arrive_time, pickup_distance, pickup_place, pickup_country, pickup_city, pickup_address, pickup_geo_long, pickup_geo_lat, price_offer, chat_available, car_model, car_color, car_plate, car_number_seat, number_people, radius = None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None

        user_id = data['user_id']

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

        if 'target_place' in data:
            target_place = data['target_place']
        if 'target_country' in data:
            target_country = data['target_country']
        if 'target_city' in data:
            target_city = data['target_city']
        if 'target_street' in data:
            target_street = data['target_street']
        if 'target_geo_long' in data:
            target_geo_long = float(data['target_geo_long'])
        if 'target_geo_lat' in data:
            target_geo_lat = float(data['target_geo_lat'])

        if 'go_date' in data:
            go_date = data['go_date']
        if 'go_time' in data:
            go_time = data['go_time']
        if 'arrive_date' in data:
            arrive_date = data['arrive_date']
        if 'arrive_time' in data:
            arrive_time = data['arrive_time']

        if 'pickup_distance' in data:
            pickup_distance = float(data['pickup_distance'])
        if 'pickup_place' in data:
            pickup_place = data['pickup_place']
        if 'pickup_country' in data:
            pickup_country = data['pickup_country']
        if 'pickup_city' in data:
            pickup_city = data['pickup_city']
        if 'pickup_address' in data:
            pickup_address = data['pickup_address']
        if 'pickup_geo_long' in data:
            pickup_geo_long = float(data['pickup_geo_long'])
        if 'pickup_geo_lat' in data:
            pickup_geo_lat = float(data['pickup_geo_lat'])

        if 'price_offer' in data:
            price_offer = data['price_offer']
        if 'chat_available' in data:
            chat_available = bool(data['chat_available'])

        if 'car_model' in data:
            car_model = data['car_model']
        if 'car_color' in data:
            car_color = data['car_color']
        if 'car_plate' in data:
            car_plate = data['car_plate']
        if 'car_number_seat' in data:
            car_number_seat = int(data['car_number_seat'])
        if 'number_people' in data:
            number_people = data['number_people']
        if 'radius' in data:
            radius = data['radius']

        if driver is None:
            driver = Driver(user_id=user_id, current_place=current_place, current_country=current_country,
                            current_city=current_city, current_street=current_street,
                            current_geo_long=current_geo_long, current_geo_lat=current_geo_lat,
                            target_place=target_place, target_country=target_country, target_city=target_city,
                            target_street=target_street, target_geo_long=target_geo_long, target_geo_lat=target_geo_lat,
                            go_date=go_date, go_time=go_time,
                            arrive_date=arrive_date, arrive_time=arrive_time,
                            pickup_distance=pickup_distance, pickup_place=pickup_place, pickup_country=pickup_country,
                            pickup_city=pickup_city, pickup_address=pickup_address,
                            pickup_geo_long=pickup_geo_long, pickup_geo_lat=pickup_geo_lat, price_offer=price_offer,
                            chat_available=chat_available, car_model=car_model,
                            car_color=car_color, car_plate=car_plate, car_number_seat=car_number_seat, number_people=number_people, radius=radius)
        else:
            driver.user_id = user_id

            driver.current_place = current_place
            driver.current_country = current_country
            driver.current_city = current_city
            driver.current_street = current_street
            driver.current_geo_long = current_geo_long
            driver.current_geo_lat = current_geo_lat

            driver.target_place = target_place
            driver.target_country = target_country
            driver.target_city = target_city
            driver.target_street = target_street
            driver.target_geo_long = target_geo_long
            driver.target_geo_lat = target_geo_lat

            driver.go_date = go_date
            driver.go_time = go_time
            driver.arrive_date = arrive_date
            driver.arrive_time = arrive_time

            driver.pickup_distance = pickup_distance
            driver.pickup_place = pickup_place
            driver.pickup_country = pickup_country
            driver.pickup_city = pickup_city
            driver.pickup_address = pickup_address
            driver.pickup_geo_long = pickup_geo_long
            driver.pickup_geo_lat = pickup_geo_lat

            driver.price_offer = price_offer
            driver.chat_available = chat_available

            driver.car_model = car_model
            driver.car_color = car_color
            driver.car_plate = car_plate
            driver.car_number_seat = car_number_seat
            driver.number_people = number_people
            driver.radius = radius
        return driver
