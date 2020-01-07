from flask_restplus import Namespace, fields
from app.modules.common.dto import Dto


class DtoCarpooling(Dto):
    name = 'carpooling'
    api = Namespace(name)
    model = api.model(name, {
        'carpooling_id':fields.Integer(required=False),
        'driver_id': fields.Integer(required=False),
        'passenger_id': fields.Integer(required=False),

        'date_created': fields.Date(required=False),
        'time_created': fields.DateTime(required=False),
        'accepted': fields.Boolean(required=False),
        'status': fields.String(required=False),

        'price_offer_passenger': fields.String(required=False),
        'price_offer_driver': fields.Float(required=False),
        'price': fields.Float(required=False),
        'rate': fields.Integer(required=False),

        'comment': fields.String(required=False)
    })
