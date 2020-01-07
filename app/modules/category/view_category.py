from flask import request
from flask_restplus import Resource

from app.modules.category.dto_category import DtoCategory
from .controller_category import ControllerCategory # create_category, get_list_category, update_category, delete_category
from app.modules.common.decorator import admin_token_required, token_required

api = DtoCategory.api
model = DtoCategory.model


# api = Routing.route_category


# @api.route('')
@api.route('')
class CategoryList(Resource):

    @token_required
    def get(self):
        controllerCategory = ControllerCategory()
        return controllerCategory.get() # _list_category()

    @admin_token_required
    @api.expect(model, validate=True)
    def post(self):
        data = request.json
        controllerCategory = ControllerCategory()
        return controllerCategory.create(data) #model_auth(data)

    @admin_token_required
    def put(self):
        data = request.json
        controllerCategory = ControllerCategory()
        return controllerCategory.update(data) #model_auth(data)

    @admin_token_required
    def delete(self):
        data = request.json
        controllerCategory = ControllerCategory()
        return controllerCategory.delete(data) # model_auth(data)
