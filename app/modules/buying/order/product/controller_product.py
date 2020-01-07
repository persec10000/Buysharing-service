from app.app import db
from app.modules.common.controller import Controller
from app.utils.response import error
from .product import Product


class ControllerProduct(Controller):

    def create(self, data):
        if not isinstance(data, dict):
            return error(message='Check data format!')
        if not 'order_id' in data:
            return error(message="Data does not consist information of buyer.")
        try:
            product = self._parse_product(data=data)
            db.session.add(product)
            db.session.commit()
            return product
            # return send_result(message="Create products successfully!")
        except Exception as e:
            # return send_error(message="Could not create product!")
            print(e.__str__())
            return None

    def get(self):
        products = Product.query.all()
        return products
        # data = marshal(products, ProductDto.model_auth)
        # return send_result(data=data, message="Get list of products successfully.")

    def get_by_id(self, object_id):
        product = Product.query.filter_by(product_id=object_id).first()
        return product

    def get_by_oder_id(self, order_id):
        products = Product.query.filter_by(order_id=order_id).all()
        return products

    def delete_by_order_id(self, order_id):
        product_delete = Product.__table__.delete().where(Product.order_id == order_id)
        db.session.execute(product_delete)
        db.session.commit()
        return True

    def update(self, object_id, data):
        try:
            product = Product.query.filter_by(product_id=object_id).first()
            if product is None:
                return False
            product = self._parse_product(data=data, product=product)
            db.session.commit()
            return product
        except Exception as e:
            return None

    def delete(self, object_id):
        try:
            product = Product.query.filter_by(product_id=object_id).first()
            if product is None:
                return False
            db.session.delete(product)
            db.session.commit()
            return True
        except Exception as e:
            return False

    def _parse_product(self, data, product=None):
        order_id, product_name, product_price, qrcode, barcode, vendor_name, photo_path, photo, store_name, store_address, category, volume, unit, amount = None, None, None, None, None, None, None, None, None, None, None, None, None, None
        if 'order_id' in data:
            try:
                order_id = int(data['order_id'])
            except Exception as e:
                print(e.__str__())
                pass

        if 'product_name' in data:
            product_name = data['product_name']
        if 'product_price' in data:
            product_price = float(data['product_price'])
        if 'qrcode' in data:
            qrcode = data['qrcode']
        if 'barcode' in data:
            barcode = data['barcode']
        if 'vendor_name' in data:
            vendor_name = data['vendor_name']
        if 'photo_path' in data:
            photo_path = data['photo_path']
        if 'photo' in data:
            photo = data['photo']
        if 'store_name' in data:
            store_name = data['store_name']
        if 'store_address' in data:
            store_address = data['store_address']
        if 'category' in data:
            category = data['category']
        if 'volume' in data:
            volume = data['volume']
        if 'unit' in data:
            unit = data['unit']
        if 'amount' in data:
            try:
                amount = int(data['amount'])
            except Exception as e:
                print(e.__str__())
                pass
        if product is None:
            product = Product(order_id=order_id, product_name=product_name, product_price=product_price, qrcode=qrcode,
                              barcode=barcode, vendor_name=vendor_name, photo_path=photo_path, photo=photo,
                              store_name=store_name,
                              store_address=store_address, category=category, volume=volume, unit=unit, amount=amount)
        else:
            product.order_id = order_id

            product.product_name = product_name
            product.product_price = product_price
            product.qrcode = qrcode
            product.barcode = barcode

            product.vendor_name = vendor_name
            product.photo_path = photo_path
            product.photo = photo
            product.store_name = store_name

            product.store_address = store_address
            product.category = category
            product.volume = volume
            product.unit = unit
            product.amount = amount
        return product
