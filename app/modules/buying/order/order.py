from ...common.model import Model
from app.app import db, flask_bcrypt


class Order(Model):
    __tablename__ = 'order'

    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    buyer_id = db.Column(db.Integer, db.ForeignKey('buyer.buyer_id'), nullable=True)
    buyer = db.relationship('Buyer', backref=db.backref('orders', lazy=True))

    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.supplier_id'), nullable=True)
    supplier = db.relationship('Supplier', backref=db.backref('orders', lazy=True))

    date_created = db.Column(db.Date)
    time_created = db.Column(db.Time)

    accepted = db.Column(db.Boolean)
    status = db.Column(db.String(45))

    price = db.Column(db.Float)
    rate = db.Column(db.Integer)

    comment = db.Column(db.String(255))
    ship_price_buyer = db.Column(db.Float)
    ship_price_supplier = db.Column(db.Float)
    ship_price = db.Column(db.Float)

    def __init__(self, buyer_id=None, supplier_id=None, date_created=None, time_created=None, accepted=None,
                 status=None, price=None, rate=None, comment=None, ship_price_buyer=None, ship_price_supplier=None,
                 ship_price=None):
        self.buyer_id = buyer_id
        self.supplier_id = supplier_id
        self.date_created = date_created
        self.time_created = time_created

        self.accepted = accepted
        self.status = status
        self.price = price
        self.rate = rate

        self.comment = comment
        self.ship_price_buyer = ship_price_buyer
        self.ship_price_supplier = ship_price_supplier
        self.ship_price = ship_price
