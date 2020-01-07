from ...user.user import User
from app.app import db, flask_bcrypt
from ...common.model import Model


class Driver(Model):
    __tablename__ = "driver"

    driver_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # relationship
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    user = db.relationship('User', backref=db.backref('drivers', lazy=True))

    current_place = db.Column(db.String(255))
    current_country = db.Column(db.String(80))
    current_city = db.Column(db.String(80))
    current_street = db.Column(db.String(80))
    current_geo_long = db.Column(db.Float)
    current_geo_lat = db.Column(db.Float)

    target_place = db.Column(db.String(255))
    target_country = db.Column(db.String(80))
    target_city = db.Column(db.String(80))
    target_street = db.Column(db.String(80))
    target_geo_long = db.Column(db.Float)
    target_geo_lat = db.Column(db.Float)

    go_date = db.Column(db.Date)
    go_time = db.Column(db.String(255))
    arrive_date = db.Column(db.Date)
    arrive_time = db.Column(db.String(255))

    pickup_distance = db.Column(db.Float)
    pickup_place = db.Column(db.String(80))
    pickup_country = db.Column(db.String(80))
    pickup_city = db.Column(db.String(80))
    pickup_address = db.Column(db.String(80))
    pickup_geo_long = db.Column(db.Float)
    pickup_geo_lat = db.Column(db.Float)

    price_offer = db.Column(db.Float)
    chat_available = db.Column(db.Boolean)

    car_model = db.Column(db.String(80))
    car_color = db.Column(db.String(80))
    car_plate = db.Column(db.String(80))
    car_number_seat = db.Column(db.Integer)
    number_people = db.Column(db.Integer)
    radius = db.Column(db.Float)

    def __init__(self, user_id, current_place=None, current_country=None, current_city=None, current_street=None,
                 current_geo_long=None, current_geo_lat=None, target_place=None, target_country=None, target_city=None,
                 target_street=None, target_geo_long=None, target_geo_lat=None, go_date=None, go_time=None,
                 arrive_date=None, arrive_time=None,
                 pickup_distance=None, pickup_place=None, pickup_country=None, pickup_city=None, pickup_address=None,
                 pickup_geo_long=None, pickup_geo_lat=None, price_offer=None, chat_available=None, car_model=None,
                 car_color=None, car_plate=None, car_number_seat=None, number_people=None, radius=None):
        self.user_id = user_id

        self.current_place = current_place
        self.current_country = current_country
        self.current_city = current_city
        self.current_street = current_street
        self.current_geo_long = current_geo_long
        self.current_geo_lat = current_geo_lat

        self.target_place = target_place
        self.target_country = target_country
        self.target_city = target_city
        self.target_street = target_street
        self.target_geo_long = target_geo_long
        self.target_geo_lat = target_geo_lat

        self.go_date = go_date
        self.go_time = go_time
        self.arrive_date = arrive_date
        self.arrive_time = arrive_time

        self.pickup_distance = pickup_distance
        self.pickup_place = pickup_place
        self.pickup_country = pickup_country
        self.pickup_city = pickup_city
        self.pickup_address = pickup_address
        self.pickup_geo_long = pickup_geo_long
        self.pickup_geo_lat = pickup_geo_lat

        self.price_offer = price_offer
        self.chat_available = chat_available

        self.car_model = car_model
        self.car_color = car_color
        self.car_plate = car_plate
        self.car_number_seat = car_number_seat
        self.number_people = number_people
        self.radius = radius
