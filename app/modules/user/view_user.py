# from flask import request
from flask_restplus import Resource, reqparse

from app.modules.user.dto_user import UserDto
from app.modules.common.decorator import admin_token_required, token_required
from .controller_user import \
    ControllerUser  # create_user, get_list_user, delete_user, update_user, get_list_blocked_user

api = UserDto.api
# api = Routing.route_user
_user = UserDto.model


@api.route('')
class UserList(Resource):
    # @admin_token_required
    # @api.marshal_list_with(_user)
    def get(self):
        """
        Return all the users in the systems. This function is used for administration only.
        ------------

        :return: List of users.
        """
        controllerUser = ControllerUser()
        return controllerUser.get()  # get_list_user()

    @api.expect(_user, validate=True)
    # @api.marshal_with(_user)
    def post(self):
        """
        Create new user.
        -------------
        parameters:
            name	string
            surname	string
            middlename	string
            fullname	string
            age	integer
            birthday	string($date)
            home_address	string
            home_country	string
            home_city	string
            home_street	string
            home_geo_long	number
            home_geo_lat	number
            phone	string
            email*	string
            username	string
            password*	string
            blocked	boolean
            token	string
            facebook	string
            instagram	string
            vkontakte	string
            avatar	string
            isadmin	boolean

        :return:
        """
        # data = request.json
        data = api.payload
        controllerUser = ControllerUser()
        return controllerUser.create(data)  # create_user(data)


@api.route('/<int:user_id>')
class User(Resource):
    # @token_required
    # @api.marshal_with(_user)
    def get(self, user_id):
        """
        Get all information of the user by his ID.
        -------------

        :param user_id: The ID of the user.

        :return: The user.
        """
        controller = ControllerUser()
        return controller.get_by_id(user_id=user_id)

    # @token_required
    @api.expect(_user, validate=True)
    def put(self, user_id):
        """
        Update existing user in the system by his ID.
        ---------------

        :param user_id:
        :param payload: in this payload there are all information of the user to update.

        :return: The user after updating.
        """
        data = api.payload
        controller = ControllerUser()
        return controller.update(object_id=user_id, data=data)

    # @token_required
    def delete(self, user_id):
        """
        Delete user by his ID.
        -----------------

        :param user_id: The ID of the User.

        :return: True if success and False vice versa.
        """
        controller = ControllerUser()
        controller.delete(user_id=user_id)


# @api.route('/block')
# class BlockList(Resource):
#     # @admin_token_required
#     def get(self):
#         controllerUser = ControllerUser()
#         return controllerUser.get_list_blocked_user()


# parser = reqparse.RequestParser()
# parser.add_argument('geo_long', type=float, required=False, help='Geo Longtitude')
# parser.add_argument('geo_lat', type=float, required=False, help='Geo Lattitude')
# parser.add_argument('country', type=str, required=False, help='The current country of the buyer')
# parser.add_argument('city', type=str, required=False, help='The current city of the buyer')
# parser.add_argument('street', type=str, required=False, help='The current street of the buyer')
# parser.add_argument('max_distance', required=False, help='The max distance to make search')
# parser.add_argument('mode', required=False, help='The mode of distance measures')
#
#
# @api.route('/search')
# @api.expect(parser)
# class BuyerSearchGeo(Resource):
#     # @api.marshal_list_with(_user)
#     def get(self):
#         args = parser.parse_args()
#         controller = ControllerUser()
#         return controller.search(args=args)

