from flask_restplus import Namespace, fields
from ..common.dto import Dto


class DtoComment(Dto):
    name = 'comment'
    api = Namespace(name)
    model = api.model(name, {
        'commentID': fields.Integer(required=False),
        'content': fields.String(required=True),
        'rate': fields.Integer(required=True),
        'ordererID': fields.Integer(required=True),
        'ordererName': fields.String(required=False),
        'shipperID': fields.Integer(required=True),
        'shipperName': fields.String(required=False),
        'time': fields.DateTime(required=False)
    })
