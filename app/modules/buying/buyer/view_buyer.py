from flask_restplus import Resource
from .controller_buyer import ControllerBuyer
from .dto_buyer import DtoBuyer
# from app.modules.common.decorator import token_required
from flask_restplus import reqparse
from datetime import date, time
from ...user.dto_user import UserDto

api = DtoBuyer.api
buyer = DtoBuyer.model
user = UserDto.model


@api.route('')
class BuyerList(Resource):
    # @token_required
    @api.marshal_list_with(buyer)
    def get(self):
        """
        Get all the buyers in the database.

        :return: List of buyers
        """
        controller = ControllerBuyer()
        return controller.get()

    @api.expect(buyer)
    @api.marshal_with(buyer)
    # @token_required
    def post(self):
        """
        Add new buyer to the database in the system.

        :return: New buyer created.
        """
        data = api.payload
        controller = ControllerBuyer()
        return controller.create(data=data)

    def delete(self, user_id):
        """
        Delete buyer by user_id.

        :param user_id: The user's ID.

        :return: True if success and False vice versa.
        """
        controller = ControllerBuyer()
        return controller.delete_by_user_id(user_id=user_id)


@api.route('/<int:buyer_id>')
class Buyer(Resource):
    @api.marshal_with(buyer)
    # @token_required
    def get(self, buyer_id):
        """
        Get information of the buyer by his ID.
        ---------------------

        :param buyer_id: The ID of the buyer.

        :return: The buyer.
        """
        controller = ControllerBuyer()
        return controller.get_by_id(object_id=buyer_id)

    @api.expect(buyer)
    # @token_required
    def put(self, buyer_id):
        """
        Update information for the buyer.
        ------------------
        :param buyer_id: The ID of the buyer.

        :return: The updated buyer.
        """
        data = api.payload
        controller = ControllerBuyer()
        return controller.update(object_id=buyer_id, data=data)

    # @token_required
    def delete(self, buyer_id):
        """
        Delete buyer from database by his ID.

        :param buyer_id: The ID of the buyer.

        :return: True if success and False vice versa.
        """
        controller = ControllerBuyer()
        return controller.delete(object_id=buyer_id)


parser = reqparse.RequestParser()
# parser.add_argument('geo_long', type=float, required=False, help='Geo Longtitude')
# parser.add_argument('geo_lat', type=float, required=False, help='Geo Lattitude')
# parser.add_argument('country', type=str, required=False, help='The current country of the buyer')
# parser.add_argument('city', type=str, required=False, help='The current city of the buyer')
# parser.add_argument('street', type=str, required=False, help='The current street of the buyer')

# parser.add_argument('max_distance', type=float, required=False, help='The max distance to make search')
# parser.add_argument('mode', required=False, help='The mode of distance measures')
parser.add_argument('buying_city', type=str, required=False, help='The city where to buy products')
parser.add_argument('buying_street', type=str, required=False, help='The street where to buy products')
parser.add_argument('ship_city', type=str, required=False, help='The city where to deliver the products')
parser.add_argument('ship_street', type=str, required=False, help='The street where to deliver the products')
parser.add_argument('buying_date', type=str, required=False, help='The date the buyer desires to buy something')
parser.add_argument('ship_date', type=str, required=False, help='The date the buyer desires to ship products')


# parser.add_argument('buying_time', type=time, required=False, help='The start time to buy')
# parser.add_argument('ship_time', type=time, required = False, help='The time to deliver products')


@api.route('/search')
@api.expect(parser)
class BuyerSearchGeo(Resource):
    @api.marshal_list_with(buyer)
    def get(self):
        """
        Search all buyer by buying_city, buying_street, ship_city, ship_street.
        ---------------------
        :buying_city: the city where to buy
        :buying_street: the street where to buy
        :ship_city: the city where to deliver the products
        :ship_street: the street where to deliver the products
        :buying_date: the date when buyer desires to buy something
        :ship_date: the date when products need to shipped to buyer

        :return: List of buyers
        """
        args = parser.parse_args()
        controller = ControllerBuyer()
        return controller.search(args=args)
