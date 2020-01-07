from flask_restplus import Resource
# from app.modules.common.decorator import token_required
from .dto_carpooling import DtoCarpooling
from .controller_carpooling import ControllerCarpooling

api = DtoCarpooling.api
carpooling = DtoCarpooling.model


@api.route('')
class CarpoolingList(Resource):
    # @token_required
    @api.marshal_list_with(carpooling)
    def get(self):
        controller = ControllerCarpooling()
        return controller.get()

    # @token_required
    @api.expect(carpooling)
    @api.marshal_with(carpooling)
    def post(self):
        data = api.payload
        controller = ControllerCarpooling()
        return controller.create(data=data)


@api.route('/<int:carpooling_id>')
class Carpooling(Resource):
    # @token_required
    @api.marshal_with(carpooling)
    def get(self, carpooling_id):
        controller = ControllerCarpooling()
        return controller.get_by_id(object_id=carpooling_id)

    # @token_required
    @api.expect(carpooling)
    @api.marshal_with(carpooling)
    def put(self, carpooling_id):
        data = api.payload
        controller = ControllerCarpooling()
        return controller.update(object_id=carpooling_id, data=data)

    # @token_required
    def delete(self, carpooling_id):
        controller = ControllerCarpooling()
        return controller.delete(object_id=carpooling_id)

@api.route('/search/passenger/<int:passenger_id>')
class PassengerCarpoolingList(Resource):
    @api.marshal_list_with(carpooling)
    def get(self, passenger_id):
        controller = ControllerCarpooling()
        return controller.get_by_passenger_id(passenger_id=passenger_id)

    def delete(self, passenger_id):
        controller = ControllerCarpooling()
        return controller.delete_by_passenger_id(passenger_id=passenger_id)


@api.route('/search/driver/<int:driver_id>')
class DriverCarpoolingList(Resource):
    @api.marshal_list_with(carpooling)
    def get(self, driver_id):
        print("helllo=====")
        controller = ControllerCarpooling()
        return controller.get_by_driver_id(driver_id=driver_id)

    def delete(self, driver_id):
        controller = ControllerCarpooling()
        return controller.delete_by_driver_id(driver_id=driver_id)
