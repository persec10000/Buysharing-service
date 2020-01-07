from flask_restplus import Namespace, fields
from ..common.dto import Dto


class DtoAccount(Dto):
    name = 'account'
    api = Namespace(name)
    model = api.model(name, {
        'account_id': fields.Integer(required=False),
        'user_id': fields.Integer(required=False),

        'account_name': fields.String(required=False),
        'account_number': fields.Float(required=False),
        'balance': fields.Float(required=False),

        'date_created': fields.Date(required=False),
        'card_type': fields.String(required=False),
        'card_expired_date': fields.Date(required=False),

        'card_security_number': fields.String(required=False),
        'bank_name': fields.String(required=False),
        'bank_swift': fields.String(required=False),
        'card_holder_name': fields.String(required=False)
    })
