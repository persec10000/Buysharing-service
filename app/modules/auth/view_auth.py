from flask import request
from flask_restplus import Resource

from app.modules.auth.dto_auth import DtoAuth
from .controller_auth import ControllerAuth
from app.modules.user.dto_user import UserDto

api = DtoAuth.api
# api = Routing.route_auth
model_auth = DtoAuth.model
model_user = UserDto.model


@api.route('/login')
class UserLogin(Resource):
    @api.expect(model_auth, validate=True)
    @api.marshal_with(model_user)
    def post(self):
        """
        Login user to the system.
        -------------
        :param email: the email of the user.
        :param password: the password of the user.

        :return: All information of user if he logged in and None if he did not log in.
        """
        post_data = request.json
        return ControllerAuth.login_user(data=post_data)


@api.route('/logout')
class LogoutAPI(Resource):
    def post(self):
        """
        Logout the user from the system.
        -------------

        :return:
        """
        # auth_header = request.headers.get('Authorization')
        # return ControllerAuth.logout_user(data=auth_header)
        return "You are logged out."


@api.route('/info')
class UserInfo(Resource):
    @api.marshal_with(model_user)
    def get(self):
        """
        Trả lại các thông tin về role của người dùng, order tương ứng.
        :return:
        """
        return ControllerAuth.get_logged_user(request)
