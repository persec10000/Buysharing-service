from ...user.user import User
from app.app import db, flask_bcrypt
from ...common.model import Model


class Supplier(Model):
    __tablename__ = "supplier"

    supplier_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # relationship
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    user = db.relationship('User', backref=db.backref('suppliers', lazy=True))

    buying_place = db.Column(db.String(255))
    buying_country = db.Column(db.String(255))
    buying_city = db.Column(db.String(255))
    buying_street = db.Column(db.String(255))
    buying_geo_long = db.Column(db.Float)
    buying_geo_lat = db.Column(db.Float)
    buying_date = db.Column(db.Date)  # date when supplier can come to buying place
    buying_time = db.Column(db.Time)  # time (expected) when supplier can come to buying place

    ship_place = db.Column(db.String(255))
    ship_country = db.Column(db.String(255))
    ship_city = db.Column(db.String(255))
    ship_street = db.Column(db.String(255))
    ship_geo_long = db.Column(db.Float)
    ship_geo_lat = db.Column(db.Float)
    ship_date = db.Column(db.Date)
    ship_time = db.Column(db.Time)

    # current_place = db.Column(db.String(255))
    # current_country = db.Column(db.String(255))
    # current_city = db.Column(db.String(255))
    # current_street = db.Column(db.String(255))
    # current_geo_long = db.Column(db.Float)
    # current_geo_lat = db.Column(db.Float)

    # search_radius = db.Column(db.Float)
    # search_place = db.Column(db.String(255))

    # delivery_date = db.Column(db.Date)
    # delivery_time = db.Column(db.Time)
    ship_radius = db.Column(db.Float)
    car_size = db.Column(db.Integer)
    shipping_cost = db.Column(db.Float)

    def __init__(self, user_id, buying_place=None, buying_country=None, buying_city=None, buying_street=None,
                 buying_geo_long=None, buying_geo_lat=None, buying_date=None, buying_time=None, ship_place=None,
                 ship_country=None, ship_city=None, ship_street=None, ship_geo_long=None, ship_geo_lat=None,
                 ship_date=None, ship_time=None, ship_radius=None, car_size=None, shipping_cost=None):
        self.user_id = user_id

        self.buying_place = buying_place
        self.buying_country = buying_country
        self.buying_city = buying_city
        self.buying_street = buying_street
        self.buying_geo_long = buying_geo_long
        self.buying_geo_lat = buying_geo_lat
        self.buying_date = buying_date
        self.buying_time = buying_time

        self.ship_place = ship_place
        self.ship_country = ship_country
        self.ship_city = ship_city
        self.ship_street = ship_street
        self.ship_geo_long = ship_geo_long
        self.ship_geo_lat = ship_geo_lat
        self.ship_date = ship_date
        self.ship_time = ship_time

        self.ship_radius = ship_radius
        self.car_size = car_size
        self.shipping_cost = shipping_cost
