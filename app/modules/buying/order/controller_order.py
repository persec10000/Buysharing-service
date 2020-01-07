from app.modules.common.controller import Controller
from .order import Order
from .dto_order import DtoOrder
from app.app import db
from datetime import date, time
import datetime


class ControllerOrder(Controller):
    def create(self, data):
        if not isinstance(data, dict):
            return False
        order = self._parse_order(data=data, order=None)
        db.session.add(order)
        db.session.commit()
        return order

    def get(self):
        orders = Order.query.all()
        return orders

    def get_by_id(self, object_id):
        order = Order.query.filter_by(order_id=object_id).first()
        return order

    def update(self, object_id, data):
        if not isinstance(data, dict):
            return False
        order = Order.query.filter_by(order_id=object_id).first()
        if order is None:
            return None
        order = self._parse_order(data=data, order=order)
        db.session.commit()
        return order

    def delete(self, object_id):
        order = Order.query.filter_by(order_id=object_id).first()
        if order is None:
            return False
        db.session.delete(order)
        db.session.commit()
        return True

    def get_by_buyer_id(self, buyer_id):
        if buyer_id is None or str(buyer_id).strip().__eq__(''):
            return None
        orders = Order.query.filter_by(buyer_id=buyer_id).order_by(Order.buyer_id.desc()).first()
        return orders

    def delete_by_buyer_id(self, buyer_id):
        if buyer_id is None or str(buyer_id).strip().__eq__(''):
            return None
        try:
            order_delete = Order.__table__.delete().where(Order.buyer_id == buyer_id)
            db.session.execute(order_delete)
            db.session.commit()
            return True
        except Exception as e:
            print(e.__str__())
            return False

    def get_by_supplier_id(self, supplier_id):
        if supplier_id is None or str(supplier_id).strip().__eq__(''):
            return None
        orders = Order.query.filter_by(supplier_id=supplier_id).order_by(Order.supplier_id.desc()).first()
        return orders

    def delete_by_supplier_id(self, supplier_id):
        if supplier_id is None or str(supplier_id).strip().__eq__(''):
            return False
        try:
            order_delete = Order.__table__.delete().where(Order.supplier_id == supplier_id)
            db.session.execute(order_delete)
            db.session.commit()
            return True
        except Exception as e:
            print(e.__str__())
            return False

    def _parse_order(self, data, order=None):
        buyer_id, supplier_id, date_created, time_created, accepted, status, price, rate, comment, ship_price_buyer, ship_price_supplier, ship_price = None, None, None, None, None, None, None, None, None, None, None, None
        if 'buyer_id' in data:
            try:
                buyer_id = int(data['buyer_id'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'supplier_id' in data:
            try:
                supplier_id = int(data['supplier_id'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'date_created' in data:
            try:
                date_created = date.fromisoformat(data['date_created'])
            except Exception as e:
                print(e.__str__())
                date_created = datetime.datetime.now().date()
        if 'time_created' in data:
            try:
                time_created = time.fromisoformat(data['time_created'])
            except Exception as e:
                print(e.__str__())
                time_created = datetime.datetime.now().time()

        if 'accepted' in data:
            try:
                accepted = bool(data['accepted'])
            except Exception as e:
                print(e.__str__())
                accepted = False
        if 'status' in data:
            status = data['status']
        else:
            status = 'open'
        if 'price' in data:
            try:
                price = float(data['price'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'rate' in data:
            try:
                rate = int(data['rate'])
            except Exception as e:
                print(e.__str__())
                pass

        if 'comment' in data:
            comment = data['comment']
        if 'ship_price_buyer' in data:
            try:
                ship_price_buyer = float(data['ship_price_buyer'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'ship_price_supplier' in data:
            try:
                ship_price_supplier = float(data['ship_price_supplier'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'ship_price' in data:
            try:
                ship_price = float(data['ship_price'])
            except Exception as e:
                print(e.__str__())
                pass

        if order is None:
            order = Order(buyer_id=buyer_id, supplier_id=supplier_id, date_created=date_created,
                          time_created=time_created, accepted=accepted, status=status, price=price, rate=rate,
                          comment=comment, ship_price_buyer=ship_price_buyer, ship_price_supplier=ship_price_supplier,
                          ship_price=ship_price)
        else:
            order.buyer_id = buyer_id
            order.supplier_id = supplier_id
            order.date_created = date_created
            order.time_created = time_created

            order.accepted = accepted
            order.status = status
            order.price = price
            order.rate = rate

            order.comment = comment
            order.ship_price_buyer = ship_price_buyer
            order.ship_price_supplier = ship_price_supplier
            order.ship_price = ship_price
        return order
