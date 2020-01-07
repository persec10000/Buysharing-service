from flask_restplus import Resource
from app.modules.common.decorator import token_required, admin_token_required
from .account import Account
from .dto_account import DtoAccount
from .controller_account import ControllerAccount

api = DtoAccount.api
_account = DtoAccount.model


@api.route('/')
class AccountList(Resource):
    # @token_required
    @api.marshal_list_with(_account)
    def get(self):
        controller = ControllerAccount()
        return controller.get()

    # @token_required
    @api.expect(_account)
    def post(self):
        data = api.payload
        controller = ControllerAccount()
        return controller.create(data=data)


@api.route('/<int:id>')
class Account(Resource):
    # @token_required
    @api.marshal_with(_account)
    def get(self, account_id):
        controller = ControllerAccount()
        return controller.get_by_id(object_id=account_id)

    # @token_required
    @api.expect(_account)
    def put(self, account_id):
        data = api.payload
        controller = ControllerAccount()
        return controller.update(object_id=account_id, data=data)

    # @token_required
    def delete(self, account_id):
        controller = ControllerAccount()
        return controller.delete(object_id=account_id)
