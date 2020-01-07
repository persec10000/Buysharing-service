from flask_restplus import Namespace, fields
from app.modules.common.dto import Dto


class DtoPassenger(Dto):
    name = 'passenger'
    api = Namespace(name)
    model = api.model(name, {
        'passenger_id': fields.Integer(required=False),
        'user_id': fields.Integer(required=True),

        'current_place': fields.String(required=True),
        'current_country': fields.String(),
        'current_city': fields.String(),
        'current_street': fields.String(),
        'current_geo_long': fields.Float(),
        'current_geo_lat': fields.Float(),

        'from_place': fields.String(),
        'from_country': fields.String(),
        'from_city': fields.String(),
        'from_street': fields.String(),
        'from_geo_long': fields.Float(),
        'from_geo_lat': fields.Float(),

        'to_place': fields.String(required=True),
        'to_country': fields.String(),
        'to_city': fields.String(),
        'to_street': fields.String(),
        'to_geo_long': fields.Float(),
        'to_geo_lat': fields.Float(),

        'go_date': fields.Date(required=True),
        'go_time': fields.String(),
        
        'number_people': fields.Integer(required=True),
        'radius': fields.Float(),
        'chat_available': fields.Boolean(required=False),
        'price_offer': fields.Float(required=True)
    })
