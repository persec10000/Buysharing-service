from ..common.model import Model
from app.app import db, flask_bcrypt


class Carpooling(Model):
    __tablename__ = 'carpooling'

    carpooling_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    driver_id = db.Column(db.Integer, db.ForeignKey('driver.driver_id'), nullable=True)
    driver = db.relationship('Driver', backref=db.backref('carpoolings', lazy=True))

    passenger_id = db.Column(db.Integer, db.ForeignKey('passenger.passenger_id'), nullable=True)
    passenger = db.relationship('Passenger', backref=db.backref('carpoolings', lazy=True))

    date_created = db.Column(db.Date)
    time_created = db.Column(db.Time)
    accepted = db.Column(db.Boolean)
    status = db.Column(db.String(45))

    price_offer_passenger = db.Column(db.Float)
    price_offer_driver = db.Column(db.Float)
    price = db.Column(db.Float)
    rate = db.Column(db.Integer)
    comment = db.Column(db.String(255))

    def __init__(self, driver_id, passenger_id, date_created, time_created, accepted, status, price_offer_passenger,
                 price_offer_driver, price, rate, comment):
        self.driver_id = driver_id
        self.passenger_id = passenger_id

        self.date_created = date_created
        self.time_created = time_created
        self.accepted = accepted
        self.status = status

        self.price_offer_driver = price_offer_driver
        self.price_offer_passenger = price_offer_passenger
        self.price = price
        self.rate = rate

        self.comment = comment
