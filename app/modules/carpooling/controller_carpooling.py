from app.modules.common.controller import Controller
from app.app import db
from .carpooling import Carpooling
from .dto_carpooling import DtoCarpooling
from datetime import date, time


class ControllerCarpooling(Controller):
    def create(self, data):
        if not isinstance(data, dict):
            return False
        carpooling = self._parse_carpooling(data=data, carpooling=None)
        db.session.add(carpooling)
        db.session.commit()
        return carpooling

    def get(self):
        carpoolings = Carpooling.query.all()
        return carpoolings

    def get_by_id(self, object_id):
        carpooling = Carpooling.query.filter_by(carpooling_id=object_id).first()
        return carpooling

    def update(self, object_id, data):
        carpooling = Carpooling.query.filter_by(carpooling_id=object_id).first()
        if carpooling is None:
            return False
        if 'accepted' in data:
            carpooling.accepted = data['accepted']
        if 'passenger_id' in data:
            carpooling.passenger_id = data['passenger_id']
        if 'driver_id' in data:
            carpooling.driver_id = data['driver_id']
        db.session.commit()
        return carpooling

    def delete(self, object_id):
        carpooling = Carpooling.query.filter_by(carpooling_id=object_id).first()
        db.session.delete(carpooling)
        db.session.commit()

    def get_by_passenger_id(self, passenger_id):
        if passenger_id is None or str(passenger_id).strip().__eq__(''):
            return None
        carpooling = Carpooling.query.filter_by(passenger_id=passenger_id).order_by(Carpooling.passenger_id.desc()).first()
        return carpooling

    def delete_by_buyer_id(self, passenger_id):
        if passenger_id is None or str(passenger_id).strip().__eq__(''):
            return None
        try:
            carpooling_delete = Carpooling.__table__.delete().where(Carpooling.passenger_id == passenger_id)
            db.session.execute(carpooling_delete)
            db.session.commit()
            return True
        except Exception as e:
            print(e.__str__())
            return False

    def get_by_driver_id(self, driver_id):
        if driver_id is None or str(driver_id).strip().__eq__(''):
            return None
        carpooling = Carpooling.query.filter_by(driver_id=driver_id).order_by(Carpooling.driver_id.desc()).first()
        return carpooling

    def delete_by_supplier_id(self, driver_id):
        if driver_id is None or str(driver_id).strip().__eq__(''):
            return False
        try:
            carpooling_delete = Carpooling.__table__.delete().where(Carpooling.driver_id == driver_id)
            db.session.execute(carpooling_delete)
            db.session.commit()
            return True
        except Exception as e:
            print(e.__str__())
            return False

    def _parse_carpooling(self, data, carpooling=None):
        driver_id, passenger_id, date_created, time_created, accepted, status, price_offer_driver, price_offer_passenger, price, rate, comment = None, None, None, None, None, None, None, None, None, None, None
        if 'driver_id' in data:
            driver_id = data['driver_id']
        if 'passenger_id' in data:
            passenger_id = data['passenger_id']

        if 'date_created' in data:
            if isinstance(data['date_created'], date):
                date_created = date.fromisoformat(data['date_created'])
        if 'time_created' in data:
            if isinstance(data['time_created'], time):
                time_created = time.fromisoformat(data['time_created'])
        if 'accepted' in data:
            accepted = bool(data['accepted'])
        if 'status' in data:
            status = data['status']

        if 'price_offer_driver' in data:
            price_offer_driver = data['price_offer_driver']
        if 'price_offer_passenger' in data:
            price_offer_passenger = data['price_offer_passenger']
        if 'price' in data:
            price = data['price']
        if 'rate' in data:
            rate = data['rate']

        if 'comment' in data:
            comment = data['comment']

        if carpooling is None:
            carpooling = Carpooling(driver_id=driver_id, passenger_id=passenger_id, date_created=date_created,
                                    time_created=time_created, accepted=accepted, status=status,
                                    price_offer_passenger=price_offer_passenger, price_offer_driver=price_offer_driver,
                                    price=price, rate=rate, comment=comment)
        else:
            carpooling.driver_id = driver_id
            carpooling.passenger_id = passenger_id

            carpooling.date_created = date_created
            carpooling.time_created = time_created
            carpooling.accepted = accepted
            carpooling.status = status

            carpooling.price_offer_driver = price_offer_driver
            carpooling.price_offer_passenger = price_offer_passenger
            carpooling.price = price
            carpooling.rate = rate

            carpooling.comment = comment
        return carpooling
