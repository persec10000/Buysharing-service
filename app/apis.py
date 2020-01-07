from flask_restplus import Api
# from flask import Blueprint

# from app.modules.user.view_user import api as user_ns
# from app.modules.auth.view_auth import api as auth_ns
# from app.modules.category.view_category import api as category_ns
# from app.modules.comment.view_comment import api as comment_ns
from app.modules import ns_user, ns_account, ns_auth, ns_buyer, ns_supplier, ns_product, ns_driver, ns_passenger, \
    ns_comment, ns_carpooling, ns_order


# blueprint = Blueprint('api', __name__)

# api = Api(blueprint,
#           title='Test EXAM',
#           version='1.1',
#           description='This is my first project')

def init_api():
    api = Api(title='Buysharing APIs',
              version='1.0',
              description='Buysharing API')
    api.add_namespace(ns_user, path='/api/v1/user')
    api.add_namespace(ns_order, path='/api/v1/order')
    api.add_namespace(ns_carpooling, path='/api/v1/carpooling')
    # api.add_namespace(ns_comment, path='/api/v1/comment')
    # api.add_namespace(ns_account, path='/api/v1/account')
    api.add_namespace(ns_auth, path='/api/v1/auth')
    api.add_namespace(ns_buyer, path='/api/v1/buyer')
    api.add_namespace(ns_product, path='/api/v1/order/product')
    api.add_namespace(ns_supplier, path='/api/v1/supplier')
    api.add_namespace(ns_driver, path='/api/v1/driver')
    api.add_namespace(ns_passenger, path='/api/v1/passenger')
    return api
