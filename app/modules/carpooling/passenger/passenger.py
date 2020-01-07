from app.app import db, flask_bcrypt
from ...common.model import Model


class Passenger(Model):
    __tablename__ = "passenger"

    passenger_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # the relationship
    user_id = db.Column(db.Integer,db.ForeignKey('user.user_id'), nullable=False)
    user = db.relationship('User', backref=db.backref('passengers', lazy=True))

    current_place = db.Column(db.String(255))
    current_country = db.Column(db.String(80))
    current_city = db.Column(db.String(80))
    current_street = db.Column(db.String(80))
    current_geo_long = db.Column(db.Float)
    current_geo_lat = db.Column(db.Float)

    from_place = db.Column(db.String(255))
    from_country = db.Column(db.String(80))
    from_city = db.Column(db.String(80))
    from_street = db.Column(db.String(80))
    from_geo_long = db.Column(db.Float)
    from_geo_lat = db.Column(db.Float)


    to_place = db.Column(db.String(255))
    to_country = db.Column(db.String(80))
    to_city = db.Column(db.String(80))
    to_street = db.Column(db.String(80))
    to_geo_long = db.Column(db.Float)
    to_geo_lat = db.Column(db.Float)

    go_date = db.Column(db.Date)
    go_time = db.Column(db.String(255))

    number_people = db.Column(db.Integer)
    radius = db.Column(db.Float)
    chat_available = db.Column(db.Boolean)
    price_offer = db.Column(db.Float)


