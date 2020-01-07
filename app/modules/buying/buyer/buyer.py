from ...common.model import Model
from app.app import db
# from app.modules.buying.order.product import Product
from ..order.order import Order


class Buyer(Model):
    __tablename__ = "buyer"

    buyer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # relationship
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    user = db.relationship('User', backref=db.backref('buyers', lazy=True))

    buying_place = db.Column(db.String(255))
    buying_country = db.Column(db.String(80))
    buying_city = db.Column(db.String(80))
    buying_street = db.Column(db.String(80))
    buying_geo_long = db.Column(db.Float)
    buying_geo_lat = db.Column(db.Float)
    buying_time = db.Column(db.Time)
    buying_date = db.Column(db.Date)

    ship_place = db.Column(db.String(255))
    ship_country = db.Column(db.String(80))
    ship_city = db.Column(db.String(80))
    ship_street = db.Column(db.String(80))
    ship_geo_long = db.Column(db.Float)
    ship_geo_lat = db.Column(db.Float)
    ship_time = db.Column(db.Time)
    ship_date = db.Column(db.Date)

    current_address = db.Column(db.String(80))
    current_country = db.Column(db.String(80))
    current_city = db.Column(db.String(80))
    current_street = db.Column(db.String(80))
    current_geo_long = db.Column(db.Float)
    current_geo_lat = db.Column(db.Float)

    search_radius = db.Column(db.Float)
    search_place = db.Column(db.String(255))

    shopping_cost = db.Column(db.Float)
    shipping_cost = db.Column(db.Float)

    def __init__(self, user_id, buying_place=None, buying_country=None, buying_city=None, buying_street=None,
                 buying_geo_long=None, buying_geo_lat=None, buying_time=None, buying_date=None, ship_place=None,
                 ship_country=None, ship_city=None, ship_street=None, ship_geo_long=None,
                 ship_geo_lat=None, ship_time=None, ship_date=None, current_address=None, current_country=None,
                 current_city=None, current_street=None, current_geo_long=None, current_geo_lat=None,
                 search_radius=None, search_place=None, shopping_cost=None, shipping_cost=None):

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

        self.current_address = current_address
        self.current_country = current_country
        self.current_city = current_city
        self.current_street = current_street
        self.current_geo_long = current_geo_long
        self.current_geo_lat = current_geo_lat

        self.search_radius = search_radius
        self.search_place = search_place
        self.shopping_cost = shopping_cost
        self.shipping_cost = shipping_cost

    # def get_shopping_cost(self):
    #     cost = 0
    #     query = Product.query.with_parent(self).all()
    #     for product in query:
    #         product_price = product.product_price
    #         cost = cost + product_price
    #     return cost

    def get_shopping_cost_all_order(self):
        cost = 0
        query = Order.query.with_parent(self).all()
        if query is None or len(query)==0:
            return cost
        for order in query:
            order_price = order.price
            cost=cost+order_price
        return cost

    def get_shopping_cost_order(self, order_id):
        order = Order.query.filter_by(order_id=order_id).first()
        if order is None:
            return None
        else:
            return order.price