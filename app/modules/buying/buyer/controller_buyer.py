from app.modules.common.controller import Controller
from app.modules.user.user import User
from .buyer import Buyer
from .dto_buyer import DtoBuyer
from app.app import db
from app.utils.geo import geo_distance
from datetime import datetime, date, time


class ControllerBuyer(Controller):
    def create(self, data):
        buyer = self._parse_buyer(data=data, buyer=None)
        db.session.add(buyer)
        db.session.commit()
        # luu lai role vao bang user
        user_id = buyer.user_id
        user = User.query.filter_by(user_id=user_id).first()
        user.role = 'buyer'
        db.session.commit()
        return buyer

    def get(self):
        buyers = Buyer.query.all()
        return buyers

    def get_by_id(self, object_id):
        buyer = Buyer.query.filter_by(buyer_id=object_id).first()
        return buyer

    def update(self, object_id, data):
        buyer = Buyer.query.filter_by(buyer_id=object_id).first()
        if buyer is None:
            return False
        else:
            buyer = self._parse_buyer(data=data, buyer=buyer)
            db.session.commit()
            return buyer

    def delete_by_user_id(self, user_id):
        if user_id is None or str(user_id).strip().__eq__(''):
            return False
        try:
            delete_command = Buyer.__table__.delete().where(Buyer.user_id == user_id)
            db.session.add(delete_command)
            db.session.commit()
            return True
        except Exception as e:
            print(e.__str__())
            return False

    def delete(self, object_id):
        buyer = Buyer.query.filter_by(buyer_id=object_id).first()
        if buyer is None:
            return False
        else:
            user_id = buyer.user_id
            db.session.delete(buyer)
            db.session.commit()
            # sau khi xoa xong thi update lai role la nguoi dung thong thuong
            user = User.query.filter_by(user_id=user_id).first()
            user.role = 'user'
            db.session.commit()
            return True

    # # other functions
    # def get_by_geo(self, geo_lat, geo_long, max_distance):
    #     buyers = Buyer.query.filter_by(
    #         geo_distance((Buyer.current_geo_long, Buyer.current_geo_lat), (geo_long, geo_lat)) <= max_distance)
    #     return buyers
    #
    # def get_by_address(self, country=None, city=None, street=None):
    #     buyers = None
    #     if country is not None:
    #         buyers = Buyer.query.filter_by(Buyer.current_country == country)
    #     if city is not None:
    #         buyers = buyers.filter_by(Buyer.current_city == city)
    #     if street is not None:
    #         buyers = buyers.filter_by(Buyer.current_street == street)
    #     return buyers

    # def search(self, args):
    #     if args is None or not isinstance(args, dict):
    #         return None
    #     geo_long, geo_lat, country, city, street, max_distance, mode = None, None, None, None, None, None, None
    #     if 'geo_long' in args:
    #         geo_long = float(args['geo_long'])
    #     if 'geo_lat' in args:
    #         geo_lat = float(args['geo_lat'])
    #     if 'country' in args:
    #         country = args['country']
    #     if 'city' in args:
    #         city = args['city']
    #     if 'street' in args:
    #         street = args['street']
    #     if 'max_distance' in args:
    #         max_distance = float(args['max_distance'])
    #     if 'mode' in args:
    #         mode = args['mode']
    #
    #     if geo_long is not None and geo_lat is not None and max_distance is not None:
    #         buyers = self._get_by_geo(geo_long=geo_long, geo_lat=geo_lat, max_distance=max_distance, mode=mode)
    #     else:
    #         buyers = self._get_by_address(country=country, city=city, street=street)
    #     return buyers

    def search(self, args):
        """
        Search by buying_city, buying_street, ship_city and ship_street

        :param args: The dictionary of all params
        :return:
        """
        if not isinstance(args, dict):
            return None
        buying_city, buying_street, ship_city, ship_street, buying_date, ship_date = None, None, None, None, None, None
        if 'buying_city' in args:
            buying_city = args['buying_city']
        if 'buying_street' in args:
            buying_street = args['buying_street']
        if 'ship_city' in args:
            ship_city = args['ship_city']
        if 'ship_street' in args:
            ship_street = args['ship_street']
        if 'buying_date' in args:
            try:
                buying_date = date.fromisoformat(str(args['buying_date']))
            except Exception as e:
                print(e.__str__())
                pass
        if 'ship_date' in args:
            try:
                ship_date = date.fromisoformat(str(args['ship_date']))
            except Exception as e:
                print(e.__str__())
                pass
        if buying_city is None and buying_street is None and ship_city is None and ship_street is None and buying_date is None and ship_date is None:
            return None
        return self._get_buyers_by_city_street(buying_city, buying_street, ship_city, ship_street,
                                               buying_date=buying_date, ship_date=ship_date)

    def _get_buyers_by_city_street(self, buying_city=None, buying_street=None, ship_city=None, ship_street=None,
                                   buying_date=None, ship_date=None):
        query = db.session.query(Buyer)
        is_filter = False
        if buying_city is not None and not str(buying_city).strip().__eq__(''):
            buying_city = '%' + buying_city.strip() + '%'
            query = query.filter(Buyer.buying_city.like(buying_city))
            is_filter = True
        if buying_street is not None and not str(buying_street).strip().__eq__(''):
            buying_street = '%' + buying_street.strip() + '%'
            query = query.filter(Buyer.buying_street.like(buying_street))
            is_filter = True
        if ship_city is not None and not str(ship_city).strip().__eq__(''):
            ship_city = '%' + ship_city.strip() + '%'
            query = query.filter(Buyer.ship_city.like(ship_city))
            is_filter = True
        if ship_street is not None and not str(ship_street).strip().__eq__(''):
            ship_street = '%' + ship_street.strip() + '%'
            query = query.filter_by(Buyer.ship_street.like(ship_street))
            is_filter = True
        if buying_date is not None and isinstance(buying_date, date):
            query = query.filter(Buyer.buying_date >= buying_date)
            is_filter = True
        if ship_date is not None and isinstance(ship_date, date):
            query = query.filter(Buyer.ship_date >= ship_date)
            is_filter = True
        if is_filter:
            buyers = query.all()
            return buyers
        else:
            return None

    # other functions
    def _get_by_geo(self, geo_lat, geo_long, max_distance, mode='km'):
        buyers = Buyer.query.all()
        ret_buyers = list()
        for buyer in buyers:
            distance = geo_distance((buyer.current_geo_long, buyer.current_geo_lat), (geo_long, geo_lat), mode=mode)
            if distance < float(max_distance):
                ret_buyers.append(buyer)
        return ret_buyers
        # users = Buyer.query.filter_by(
        #     geo_distance((Buyer.current_geo_long, Buyer.current_geo_lat), (geo_long, geo_lat),
        #                  mode=mode) <= max_distance).all()
        # return users

    def _get_by_address(self, country=None, city=None, street=None):
        query = db.session.query(Buyer)
        # users = None
        if country is not None:
            # users = User.query.filter_by(home_country=country).all()
            query = query.filter_by(Buyer.home_country.like(country))
        if city is not None:
            # users = users.filter_by(home_city=city).all()
            query = query.filter_by(home_city=city)
        if street is not None:
            # users = users.filter_by(home_street=street).all()
            query = query.filter_by(home_street=street)
        users = query.all()
        return users

    def _parse_buyer(self, data, buyer=None):
        user_id, buying_place, buying_country, buying_city, buying_street, buying_geo_long, buying_geo_lat, buying_time, buying_date, ship_place, ship_country, ship_city, ship_street, ship_geo_long, ship_geo_lat, ship_time, ship_date, current_address, current_country, current_city, current_street, current_geo_long, current_geo_lat, search_radius, search_place, shopping_cost, shipping_cost = None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None

        user_id = data['user_id']

        if 'buying_place' in data:
            buying_place = str(data['buying_place'])
        if 'buying_country' in data:
            buying_country = str(data['buying_country'])
        if 'buying_city' in data:
            buying_city = str(data['buying_city'])
        if 'buying_street' in data:
            buying_street = str(data['buying_street'])
        if 'buying_geo_long' in data:
            buying_geo_long = float(data['buying_geo_long'])
        if 'buying_geo_lat' in data:
            buying_geo_lat = float(data['buying_geo_lat'])
        if 'buying_date' in data:
            try:
                buying_date = date.fromisoformat(data['buying_date'])
            except Exception as e:
                print(e.__str__())
                buying_date = datetime.now().date()
        if 'buying_time' in data:
            try:
                buying_time = time.fromisoformat(data['buying_time'])
            except Exception as e:
                print(e.__str__())
                buying_time = datetime.now().time()

        if 'ship_place' in data:
            ship_place = data['ship_place']
        if 'ship_country' in data:
            ship_country = data['ship_country']
        if 'ship_city' in data:
            ship_city = data['ship_city']
        if 'ship_street' in data:
            ship_street = data['ship_street']
        if 'ship_geo_long' in data:
            ship_geo_long = float(data['ship_geo_long'])  # xu ly ngoai le cho nay sau
        if 'ship_geo_lat' in data:
            ship_geo_lat = float(data['ship_geo_lat'])
        if 'ship_date' in data:
            try:
                ship_date = date.fromisoformat(data['ship_date'])
            except Exception as e:
                print(e.__str__())
                ship_date = datetime.now().date()
        if 'ship_time' in data:
            try:
                ship_time = time.fromisoformat(data['ship_time'])
            except Exception as e:
                print(e.__str__())
                ship_time = datetime.now().time()

        if 'current_address' in data:
            current_address = data['current_address']
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

        if 'search_radius' in data:
            search_radius = float(data['search_radius'])
        if 'search_place' in data:
            search_place = data['search_place']
        if 'shopping_cost' in data:
            shopping_cost = float(data['shopping_cost'])
        if 'shipping_cost' in data:
            shipping_cost = float(data['shipping_cost'])

        if buyer is None:
            buyer = Buyer(user_id=user_id, buying_place=buying_place, buying_country=buying_country,
                          buying_city=buying_city, buying_street=buying_street, buying_geo_long=buying_geo_long,
                          buying_geo_lat=buying_geo_lat, buying_time=buying_time, buying_date=buying_date,
                          ship_place=ship_place, ship_country=ship_country, ship_city=ship_city,
                          ship_street=ship_street, ship_geo_long=ship_geo_long,
                          ship_geo_lat=ship_geo_lat, ship_time=ship_time, ship_date=ship_date,
                          current_address=current_address, current_country=current_country, current_city=current_city,
                          current_street=current_street, current_geo_long=current_geo_long,
                          current_geo_lat=current_geo_lat, search_radius=search_radius, search_place=search_place,
                          shopping_cost=shopping_cost, shipping_cost=shipping_cost)
        else:
            # buyer.user_id, buyer.buying_place, buyer.buying_time, buyer.buying_date, buyer.desired_place_ship, buyer.desired_time_ship, buyer.desired_date_ship, buyer.search_radius, buyer.search_place, buyer.shopping_cost, buyer.shipping_cost = user_id, buying_place, buying_time, buying_date, desired_place_ship, desired_time_ship, desired_date_ship, search_radius, search_place, shopping_cost, shipping_cost
            # buyer.order_id =
            buyer.user_id = user_id

            buyer.buying_place = buying_place
            buyer.buying_country = buying_country
            buyer.buying_city = buying_city
            buyer.buying_street = buying_street
            buyer.buying_geo_long = buying_geo_long
            buyer.buying_geo_lat = buying_geo_lat
            buyer.buying_time = buying_time
            buyer.buying_date = buying_date

            buyer.ship_place = ship_place
            buyer.ship_country = ship_country
            buyer.ship_city = ship_city
            buyer.ship_street = ship_street
            buyer.ship_geo_long = ship_geo_long
            buyer.ship_geo_lat = ship_geo_lat
            buyer.ship_time = ship_time
            buyer.ship_date = ship_date

            buyer.current_address = current_address
            buyer.current_country = current_country
            buyer.current_city = current_city
            buyer.current_street = current_street
            buyer.current_geo_long = current_geo_long
            buyer.current_geo_lat = current_geo_lat

            buyer.search_radius = search_radius
            buyer.search_place = search_place
            buyer.shopping_cost = shopping_cost
            buyer.shipping_cost = shipping_cost
        return buyer
