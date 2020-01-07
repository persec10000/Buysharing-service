from flask_restplus import Namespace, fields
from ...common.dto import Dto


class DtoDriver(Dto):
    name = 'driver'
    api = Namespace(name)
    model = api.model(name, {
        'driver_id': fields.Integer(required=False),
        'user_id': fields.Integer(required=True),

        'current_place': fields.String(required=False),
        'current_country': fields.String(required=False),
        'current_city': fields.String(required=False),
        'current_street': fields.String(required=False),
        'current_geo_long': fields.Float(required=False),
        'current_geo_lat': fields.Float(required=False),

        'target_place': fields.String(required=False),
        'target_country': fields.String(required=False),
        'target_city': fields.String(required=False),
        'target_street': fields.String(required=False),
        'target_geo_long': fields.Float(required=False),
        'target_geo_lat': fields.Float(required=False),

        'go_date': fields.Date(required=False),
        'go_time': fields.String(required=False),
        'arrive_date': fields.Date(required=False),
        'arrive_time': fields.String(required=False),

        'pickup_distance': fields.Float(required=False),
        'pickup_place': fields.String(required=False),
        'pickup_country': fields.String(required=False),
        'pickup_city': fields.String(required=False),
        'pickup_address': fields.String(required=False),
        'pickup_geo_long': fields.Float(required=False),
        'pickup_geo_lat': fields.Float(required=False),

        'price_offer': fields.Float(required=False),
        'chat_available': fields.Boolean(required=False),
        'car_model': fields.String(required=False),
        'car_color': fields.String(required=False),
        'car_plate': fields.String(required=False),
        'car_number_seat': fields.Integer(required=False),
        'number_people': fields.Integer(required=False),
        'radius': fields.Float(required=False)
    })
    # submodel = api.model(name, {
    #     'price_offer': fields.Float(required=False),
    #     'car_model': fields.String(required=False),
    #     'car_color': fields.String(required=False),
    #     'car_plate': fields.String(required=False),
    # })
