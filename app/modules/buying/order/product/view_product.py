from flask_restplus import Resource

# from app.modules.common.decorator import token_required
from .controller_product import ControllerProduct
from .dto_product import ProductDto

api = ProductDto.api
product = ProductDto.model


@api.route('')
class ProductList(Resource):
    # @token_required
    @api.marshal_list_with(product)
    def get(self):
        """
        Return all products in table.

        :return: List of products
        """
        controller = ControllerProduct()
        return controller.get()

    @api.expect(product)
    @api.marshal_with(product)
    # @token_required
    def post(self):
        """
        Create new product to save to database and return it to client.

        :return: New product.
        """
        data = api.payload
        controller = ControllerProduct()
        return controller.create(data=data)

    # def delete(self, order_id):
    #     """
    #     Delete all products belong to order when order is deleted.
    #
    #     :param order_id: The order ID.
    #
    #     :return:
    #     """


@api.route('/<int:product_id>')
@api.response(404, "Product not found")
@api.param('product_id', 'The product identifer')
class Product(Resource):
    @api.marshal_with(product)
    # @token_required
    def get(self, product_id):
        """
        Get information about product by its ID.

        :param product_id: The ID of product.

        :return: The product information.
        """
        controller = ControllerProduct()
        return controller.get_by_id(object_id=product_id)

    @api.expect(product)
    @api.marshal_with(product)
    # @token_required
    def put(self, product_id):
        """
        Update information of product.

        :param product_id: The ID of product.

        :return: The product after editing.
        """
        data = api.payload
        controller = ControllerProduct()
        return controller.update(object_id=product_id, data=data)

    # @token_required
    def delete(self, product_id):
        """
        Delete product in database.

        :param product_id: The ID of the product to delete.

        :return: True if success and False vice versa.
        """
        controller = ControllerProduct()
        return controller.delete(object_id=product_id)


@api.route('/order/<int:order_id>')
class OrderProductList(Resource):
    @api.marshal_list_with(product)
    def get(self, order_id):
        """
        Return all products by order_id

        :param order_id: The ID of the order

        :return: The list of products.
        """
        controller = ControllerProduct()
        return controller.get_by_oder_id(order_id=order_id)

    def delete(self, order_id):
        """
        Delete all products by order_id.

        :param order_id: The ID of the order.

        :return:
        """
        controller = ControllerProduct()
        return controller.delete_by_order_id(order_id=order_id)
