from app.modules.common.dto import Dto
from flask_restplus import Namespace, fields


class ProductDto(Dto):
    name = 'product'
    api = Namespace(name=name)
    model = api.model(name, {
        'product_id': fields.Integer(required=False),
        # 'order_id': fields.Integer(required=True),
        'order_id': fields.Integer(required=True),

        'product_name': fields.String(required=False),
        'product_price': fields.Float(required=False),
        # 'qrcode': fields.String(required=False),

        # 'barcode': fields.String(required=False),
        'vendor_name': fields.String(required=False),
        # 'photo_path': fields.String(required=False),
        'photo': fields.String(required=False),
        # 'store_name': fields.String(required=False),

        # 'store_address': fields.String(required=False),
        # 'category': fields.String(required=False),
        'volume': fields.String(required=False),
        'unit': fields.String(required=False),
        'amount': fields.Integer(required=False)
    })
