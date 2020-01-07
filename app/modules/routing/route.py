from flask_restplus import Namespace


class Routing:
    """
    This class is used to route to resource
    """
    route_user = Namespace('user')
    route_auth = Namespace('auth')
    route_category = Namespace('category')
    route_comment = Namespace('comment')