from flask_restplus import Namespace, fields
from ...common.dto import Dto


class DtoSupplier(Dto):
    name = 'supplier'
    api = Namespace(name)
    model = api.model(name, {
        'supplier_id': fields.Integer(required=False),
        'user_id': fields.Integer(required=True),
        'username': fields.String(required=False, attribute='user.username'),
        'fullname': fields.String(required=False, attribute='user.fullname'),
        'avatar': fields.String(required=False, attribute='user.avatar'),
        'phone': fields.String(required=False, attribute='user.phone'),

        'buying_place': fields.String(required=False),
        'buying_country': fields.String(required=False),
        'buying_city': fields.String(required=False),
        'buying_street': fields.String(required=False),
        'buying_geo_long': fields.Float(required=False),
        'buying_geo_lat': fields.Float(required=False),
        'buying_date': fields.Date(required=False),
        'buying_time': fields.String(required=False),

        'ship_place': fields.String(required=False),
        'ship_country': fields.String(required=False),
        'ship_city': fields.String(required=False),
        'ship_street': fields.String(required=False),
        'ship_geo_long': fields.Float(required=False),
        'ship_geo_lat': fields.Float(required=False),
        'ship_date': fields.Date(required=False),
        'ship_time': fields.String(required=False),

        'ship_radius': fields.Float(required=False),
        'car_size': fields.Integer(required=False),
        'shipping_cost': fields.Float(required=False)
    })
