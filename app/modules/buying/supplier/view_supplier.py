from flask_restplus import Resource, reqparse
# from app.modules.common.decorator import token_required
from .controller_supplier import ControllerSupplier
from .dto_supplier import DtoSupplier
from ...user.dto_user import UserDto

api = DtoSupplier.api
supplier = DtoSupplier.model
user = UserDto.model


@api.route('')
class SupplierList(Resource):
    # @token_required
    @api.marshal_list_with(supplier)
    def get(self):
        """
        Get all suppliers in database
        --------------
        :return: List of suppliers
        """
        controller = ControllerSupplier()
        return controller.get()

    # @token_required
    @api.expect(supplier)
    @api.marshal_with(supplier)
    def post(self):
        """
        Create new supplier.

        :return: New supplier which created
        """
        controller = ControllerSupplier()
        data = api.payload
        return controller.create(data=data)

    def delete(self, user_id):
        """
        Delete suppliers belong to user by user_id.
        --------------------
        :param user_id: The user's ID.

        :return: True if success and False vice versa.
        """
        controller = ControllerSupplier()
        controller.delete_by_user_id(user_id=user_id)


@api.route('/<int:supplier_id>')
class Supplier(Resource):
    # @token_required
    @api.marshal_with(supplier)
    def get(self, supplier_id):
        """
        Get all information about supplier by his ID.
        ----------------

        :param supplier_id: The ID of supplier.

        :return: The supplier.
        """
        controller = ControllerSupplier()
        return controller.get_by_id(object_id=supplier_id)

    # @token_required
    @api.expect(supplier)
    @api.marshal_with(supplier)
    def put(self, supplier_id):
        """
        Update information to supplier.
        -------------

        :param supplier_id: The ID of the supplier to update.

        :return: The supplier after updating.
        """
        data = api.payload
        controller = ControllerSupplier()
        return controller.update(object_id=supplier_id, data=data)

    # @token_required
    def delete(self, supplier_id):
        """
        Delete Supplier from database by his ID.
        -----------------

        :param supplier_id: The ID of the supplier.

        :return: True if success and False vice versa.
        """
        controller = ControllerSupplier()
        return controller.delete(object_id=supplier_id)


parser = reqparse.RequestParser()
# parser.add_argument('geo_long', type=float, required=False, help='Geo Longtitude of the supplier')
# parser.add_argument('geo_lat', type=float, required=False, help='Geo Lattitude of the supplier')
# parser.add_argument('country', type=str, required=False, help='The buying country of the supplier')
parser.add_argument('buying_city', type=str, required=False, help='The buying city of the supplier')
parser.add_argument('buying_street', type=str, required=False, help='The buying street of the supplier')
parser.add_argument('ship_city', type=str, required=False, help='The ship city (or destination city) of the supplier')
parser.add_argument('ship_street', type=str, required=False,
                    help='The ship street (or destination street) of the supplier')
parser.add_argument('buying_date', type=str, required=False, help='The date to buy')
parser.add_argument('ship_date', type=str, required=False, help='The date to ship')


# parser.add_argument('buying_geo_long', type=float, required=False, help='The buying geo longtitude location')
# parser.add_argument('buying_geo_lat', type=float, required=False, help='The buying geo latitude location')
# parser.add_argument('ship_geo_long', type=float, required=False, help='The ship geo longtitude location')
# parser.add_argument('ship_geo_lat', type=float, required=False, help='The ship geo latitude location')


# parser.add_argument('max_distance', required=False, help='The max distance to make search')
# parser.add_argument('mode', required=False, help='The mode of distance measures')


@api.route('/search')
@api.expect(parser)
class SupplierSearchGeo(Resource):
    @api.marshal_list_with(supplier)
    def get(self):
        """
        Get list of suppliers who satisfy the search conditions.
        ----------------------
        Request params:
        :buying_city: the buying city of supplier (or city that supplier will appear in the near ship)
        :buying_street: The buying street of the supplier (or street that supplier will appear in the near ship)
        :ship_city: the ship city of supplier (or destination city where supplier can come)
        :ship_street: the ship street of supplier (or destination street where supplier can come)

        :return: List of suppliers
        """
        args = parser.parse_args()
        controller = ControllerSupplier()
        return controller.search(args=args)
