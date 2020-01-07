from flask_restplus import Resource
from .dto_order import DtoOrder
from .controller_order import ControllerOrder

# from app.modules.common.decorator import token_required

api = DtoOrder.api
order = DtoOrder.model


@api.route('')
class OrderList(Resource):
    # @token_required
    @api.marshal_list_with(order)
    def get(self):
        """
        Get all orders in database.
        -----------------

        :return: List of orders.
        """
        controller = ControllerOrder()
        return controller.get()

    # @token_required
    @api.expect(order)
    @api.marshal_with(order)
    def post(self):
        """
        Create new order and save to database.
        -----------------
        :return: New order which has been created.
        """
        data = api.payload
        controller = ControllerOrder()
        return controller.create(data=data)


@api.route('/<int:order_id>')
class Order(Resource):
    # @token_required
    @api.marshal_with(order)
    def get(self, order_id):
        """
        Get all information about order by its ID.
        -------------------
        :param order_id: The ID of the order.

        :return: The order.
        """
        controller = ControllerOrder()
        return controller.get_by_id(object_id=order_id)

    # @token_required
    @api.expect(order)
    @api.marshal_with(order)
    def put(self, order_id):
        """
        Update existing order by its ID.
        ----------------

        :param order_id: The ID of the order.

        :return: The order after updating.
        """
        data = api.payload
        controller = ControllerOrder()
        return controller.update(object_id=order_id, data=data)

    # @token_required
    def delete(self, order_id):
        """
        Delete order in database by its ID.

        :param order_id: The ID of the order.

        :return: True if success and False vice versa.
        """
        controller = ControllerOrder()
        return controller.delete(object_id=order_id)


@api.route('/search/buyer/<int:buyer_id>')
class BuyerOrderList(Resource):
    @api.marshal_list_with(order)
    def get(self, buyer_id):
        """
        Get all orders of buyer by buyer_id

        :param buyer_id: The ID of the buyer.

        :return: List of orders.
        """
        controller = ControllerOrder()
        return controller.get_by_buyer_id(buyer_id=buyer_id)

    def delete(self, buyer_id):
        """
        Delete all orders of buyer by buyer_id.

        :param buyer_id: The ID of the buyer.

        :return: True if success and False vice versa.
        """
        controller = ControllerOrder()
        return controller.delete_by_buyer_id(buyer_id=buyer_id)


@api.route('/search/supplier/<int:supplier_id>')
class OrderProductList(Resource):
    @api.marshal_list_with(order)
    def get(self, supplier_id):
        """
        Get all orders of supplier by supplier_id.

        :param supplier_id: The ID of the supplier.

        :return: List of orders.
        """
        controller = ControllerOrder()
        return controller.get_by_supplier_id(supplier_id=supplier_id)

    def delete(self, supplier_id):
        """
        Delete orders of supplier by supplier_id.

        :param supplier_id: The ID of the supplier.

        :return: True if success and False vice versa.
        """
        controller = ControllerOrder()
        return controller.delete_by_supplier_id(supplier_id=supplier_id)
