from flask_restplus import Resource, reqparse
# from app.modules.common.decorator import token_required, admin_token_required

from .controller_passenger import ControllerPassenger
from .dto_passenger import DtoPassenger

api = DtoPassenger.api
passenger = DtoPassenger.model


@api.route('')
class PassengerList(Resource):
    # @token_required
    @api.marshal_list_with(passenger)
    def get(self):
        controller = ControllerPassenger()
        return controller.get()

    # @token_required
    @api.expect(passenger)
    @api.marshal_with(passenger)
    def post(self):
        data = api.payload
        controller = ControllerPassenger()
        return controller.create(data=data)


@api.route('/<int:passenger_id>')
@api.param('passenger_id', 'The passenger identifier')
class Passenger(Resource):
    # @token_required
    @api.marshal_with(passenger)
    def get(self, passenger_id):
        controller = ControllerPassenger()
        return controller.get_by_id(object_id=passenger_id)

    # @token_required
    @api.expect(passenger)
    @api.marshal_with(passenger)
    def put(self, passenger_id):
        data = api.payload
        controller = ControllerPassenger()
        return controller.update(object_id=passenger_id, data=data)

    # @token_required
    def delete(self, passenger_id):
        controller = ControllerPassenger()
        return controller.delete(object_id=passenger_id)


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
class PassengerSearchGeo(Resource):
    @api.marshal_list_with(passenger)
    def get(self):
        args = parser.parse_args()
        controller = ControllerPassenger()
        return controller.search(args=args)
