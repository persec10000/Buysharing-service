from flask_restplus import Resource, reqparse
from .dto_driver import DtoDriver
from .controller_driver import ControllerDriver
# from app.modules.common.decorator import token_required

api = DtoDriver.api
driver = DtoDriver.model
# subdriver = DtoDriver.submodel


@api.route('')
class DriverList(Resource):
    @api.marshal_list_with(driver)
    # @token_required
    def get(self):
        controller = ControllerDriver()
        return controller.get()

    # @token_required
    @api.expect(driver)
    @api.marshal_with(driver)
    def post(self):
        data = api.payload
        controller = ControllerDriver()
        return controller.create(data=data)


@api.route('/<int:driver_id>')
class Driver(Resource):
    # @token_required
    @api.marshal_with(driver)
    def get(self, driver_id):
        controller = ControllerDriver()
        return controller.get_by_id(object_id=driver_id)

    # @token_required
    @api.expect(driver)
    @api.marshal_with(driver)
    def put(self, driver_id):
        data = api.payload
        controller = ControllerDriver()
        return controller.update(object_id=driver_id, data=data)

    # @token_required
    def delete(self, driver_id):
        controller = ControllerDriver()
        return controller.delete(object_id=driver_id)


parser = reqparse.RequestParser()
parser.add_argument('geo_long', type=float, required=False, help='Geo Longtitude')
parser.add_argument('geo_lat', type=float, required=False, help='Geo Lattitude')
parser.add_argument('country', type=str, required=False, help='The current country of the buyer')
parser.add_argument('city', type=str, required=False, help='The current city of the buyer')
parser.add_argument('street', type=str, required=False, help='The current street of the buyer')
parser.add_argument('max_distance', required=False, help='The max distance to make search')
parser.add_argument('mode', required=False, help='The mode of distance measures')


@api.route('/search')
@api.expect(parser)
class DriverSearchGeo(Resource):
    @api.marshal_list_with(driver)
    def get(self):
        args = parser.parse_args()
        controller = ControllerDriver()
        return controller.search(args=args)
