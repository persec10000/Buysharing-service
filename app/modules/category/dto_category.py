from flask_restplus import Namespace, fields
from ..common.dto import Dto


class DtoCategory(Dto):
    api = Namespace('category')
    model = api.model('category', {
        'categoryID': fields.Integer(required=False),
        'categoryName': fields.String(required=True),
    })
