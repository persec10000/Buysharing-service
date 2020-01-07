from app.modules.common.controller import Controller
from app.app import db
from app.modules.user.user import User
from .supplier import Supplier
from ...user.user import User
from app.utils.geo import geo_distance
from datetime import datetime, date, time


class ControllerSupplier(Controller):

    # Thao tac tren list
    def create(self, data):
        supplier = self._parse_supplier(data=data, supplier=None)
        db.session.add(supplier)
        db.session.commit()
        user_id = supplier.user_id
        user = User.query.filter_by(user_id=user_id).first()
        user.role = 'supplier'
        db.session.commit()
        return supplier

    def get(self):
        suppliers = Supplier.query.all()
        return suppliers

    def get_by_id(self, object_id):
        supplier = Supplier.query.filter_by(supplier_id=object_id).first()
        return supplier

    def update(self, object_id, data):
        supplier = Supplier.query.filter_by(supplier_id=object_id).first()
        if supplier is None:
            return None
        else:
            supplier = self._parse_supplier(data=data, supplier=supplier)
            db.session.commit()
            return supplier

    def delete(self, object_id):
        supplier = Supplier.query.filter_by(supplier_id=object_id).first()
        if supplier is None:
            return False
        else:
            user_id = supplier.user_id
            # xoa supplier
            db.session.delete(supplier)
            db.session.commit()
            # cap nhat lai vai tro
            user = User.query.filter_by(user_id=user_id).first()
            user.role = 'user'
            db.session.commit()
            return True

    def delete_by_user_id(self, user_id):
        """
        Delete suppliers belong to user by user's ID.

        :param user_id: The user's ID.

        :return: True if success and False vice versa.
        """
        if user_id is None or str(user_id).strip().__eq__(''):
            return False
        try:
            delete_command = Supplier.__table__.delete().where(Supplier.user_id == user_id)
            db.session.add(delete_command)
            db.session.commit()
            return True
        except Exception as e:
            print(e.__str__())
            return False

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
        return self._get_suppliers_by_city_street(buying_city, buying_street, ship_city, ship_street, buying_date,
                                                  ship_date)

    def _get_suppliers_by_city_street(self, buying_city=None, buying_street=None, ship_city=None,
                                      ship_street=None, buying_date=None, ship_date=None):
        query = db.session.query(Supplier)
        is_filter = False
        if buying_city is not None and not str(buying_city).strip().__eq__(''):
            buying_city = '%' + buying_city.strip() + '%'
            query = query.filter(Supplier.buying_city.like(buying_city))
            is_filter = True
        if buying_street is not None and not str(buying_street).strip().__eq__(''):
            buying_street = '%' + buying_street.strip() + '%'
            query = query.filter(Supplier.buying_street.like(buying_street))
            is_filter = True
        if ship_city is not None and not str(ship_city).strip().__eq__(''):
            ship_city = '%' + ship_city.strip() + '%'
            query = query.filter(Supplier.ship_city.like(ship_city))
            is_filter = True
        if ship_street is not None and not str(ship_street).strip().__eq__(''):
            ship_street = '%' + ship_street.strip() + '%'
            query = query.filter(Supplier.ship_street.like(ship_street))
            is_filter = True
        if buying_date is not None and isinstance(buying_date, date):
            query = query.filter(Supplier.buying_date >= buying_date)
            is_filter = True
        if ship_date is not None and isinstance(ship_date, date):
            query = query.filter(Supplier.ship_date >= ship_date)
            is_filter = True
        if is_filter:
            suppliers = query.all()
            return suppliers
        else:
            return None

    # other functions
    def _get_by_geo(self, geo_lat, geo_long, max_distance, mode='km'):
        suppliers = Supplier.query.all()
        ret_suppliers = list()
        for supplier in suppliers:
            distance = geo_distance((supplier.buying_geo_long, supplier.buying_geo_lat), (geo_long, geo_lat),
                                    mode=mode)
            if distance < float(max_distance):
                ret_suppliers.append(supplier)
        return ret_suppliers

        # users = Supplier.query.filter_by(
        #     geo_distance((Supplier.buying_geo_long, Supplier.buying_geo_lat), (geo_long, geo_lat),
        #                  mode=mode) <= max_distance).all()
        # return users

    def _get_by_address(self, country=None, city=None, street=None):
        query = db.session.query(Supplier)
        # users = None
        if country is not None:
            # users = User.query.filter_by(home_country=country).all()
            query = query.filter_by(home_country=country)
        if city is not None:
            # users = users.filter_by(home_city=city).all()
            query = query.filter_by(home_city=city)
        if street is not None:
            # users = users.filter_by(home_street=street).all()
            query = query.filter_by(home_street=street)
        users = query.all()
        return users

    def _parse_supplier(self, data, supplier=None):
        user_id, buying_place, buying_country, buying_city, buying_street, buying_geo_long, buying_geo_lat, buying_date, buying_time, ship_store, ship_country, ship_city, ship_street, ship_geo_long, ship_geo_lat, ship_date, ship_time, ship_radius, car_size, shipping_cost = None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None

        user_id = data['user_id']

        if 'buying_place' in data:
            buying_place = data['buying_place']
        if 'buying_country' in data:
            buying_country = data['buying_country']
        if 'buying_city' in data:
            buying_city = data['buying_city']
        if 'buying_street' in data:
            buying_street = data['buying_street']
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
            ship_store = data['ship_place']
        if 'ship_country' in data:
            ship_country = data['ship_country']
        if 'ship_city' in data:
            ship_city = data['ship_city']
        if 'ship_street' in data:
            ship_street = data['ship_street']
        if 'ship_geo_long' in data:
            ship_geo_long = float(data['ship_geo_long'])
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

        if 'ship_radius' in data:
            delivery_radius = float(data['ship_radius'])
        if 'car_size' in data:
            car_size = int(data['car_size'])
        if 'shipping_cost' in data:
            shipping_cost = float(data['shipping_cost'])

        if supplier is None:
            supplier = Supplier(user_id=user_id, buying_place=buying_place, buying_country=buying_country,
                                buying_city=buying_city, buying_street=buying_street,
                                buying_geo_long=buying_geo_long, buying_geo_lat=buying_geo_lat, buying_date=buying_date,
                                buying_time=buying_time,
                                ship_place=ship_store, ship_country=ship_country, ship_city=ship_city,
                                ship_street=ship_street, ship_geo_long=ship_geo_long,
                                ship_geo_lat=ship_geo_lat, ship_date=ship_date, ship_time=ship_time,
                                ship_radius=ship_radius, car_size=car_size,
                                shipping_cost=shipping_cost)
        else:
            supplier.user_id = user_id

            supplier.buying_store = buying_place
            supplier.buying_country = buying_country
            supplier.buying_city = buying_city
            supplier.buying_street = buying_street
            supplier.buying_geo_long = buying_geo_long
            supplier.buying_geo_lat = buying_geo_lat
            supplier.buying_date = buying_date
            supplier.buying_time = buying_time

            supplier.ship_store = ship_store
            supplier.ship_country = ship_country
            supplier.ship_city = ship_city
            supplier.ship_street = ship_street
            supplier.ship_geo_long = ship_geo_long
            supplier.ship_geo_lat = ship_geo_lat
            supplier.ship_date = ship_date
            supplier.ship_time = ship_time

            supplier.ship_radius = ship_radius
            supplier.car_size = car_size
            supplier.shipping_cost = shipping_cost
        return supplier
