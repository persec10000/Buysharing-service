from flask_restplus import Namespace, fields
from ...common.dto import Dto


class DtoOrder(Dto):
    name = 'order'
    api = Namespace(name)
    model = api.model(name, {
        'order_id': fields.Integer(requiered=False),
        'buyer_id': fields.Integer(required=False),
        'supplier_id': fields.Integer(required=False),

        'date_created': fields.Date(required=False),
        'time_created': fields.String(required=False),

        'accepted': fields.Boolean(required=False),
        'status': fields.String(required=False),
        'price': fields.Float(required=False),
        'rate': fields.Integer(required=False),

        'comment': fields.String(required=False),
        'ship_price_buyer': fields.Float(required=False),
        'ship_price_supplier': fields.Float(required=False),
        'ship_price': fields.Float(required=False)
    })
