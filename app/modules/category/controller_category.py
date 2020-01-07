from app.app import db
from flask_restplus import marshal

from app.modules.category.category import Category

from app.utils.response import error, result
from app.modules.category.dto_category import DtoCategory
from app.modules.common.controller import Controller


class ControllerCategory(Controller):

    def create(self, data):
        try:
            exist_category = Category.query.filter_by(categoryName=data['categoryName']).first()
            if not exist_category:
                category = Category(
                    categoryName=data['categoryName'],
                )
                db.session.add(category)
                db.session.commit()
                return result(message='Create category successfully', data=marshal(category, DtoCategory.category))
            else:
                return error(message='Category already exists')
        except Exception as e:
            return error(message=e)

    def get(self):
        try:
            list_category = Category.query.all()
            return result(data=marshal(list_category, DtoCategory.category))
        except Exception as e:
            return error(message=e)

    def get_by_id(self, id):
        pass

    def update(self, data):
        try:
            category = Category.query.filter_by(categoryID=data['categoryID']).first()
            if not category:
                return error(message='Category not found')
            else:
                category.categoryName = data['categoryName']
                db.session.commit()
                return result(message='Update category successfully')
        except Exception as e:
            return error(message=e)

    def delete(self, data):
        try:
            category = Category.query.filter_by(categoryID=data['categoryID']).first()
            if not category:
                return error(message='Category not found')
            else:
                db.session.delete(category)
                db.session.commit()
                return result(message='Delete category successfully')
        except Exception as e:
            return error(message=e)


# def create_category(data):
#     try:
#         exist_category = Category.query.filter_by(categoryName=data['categoryName']).first()
#         if not exist_category:
#             category = Category(
#                 categoryName=data['categoryName'],
#             )
#             db.session.add(category)
#             db.session.commit()
#             return send_result(message='Create category successfully', data=marshal(category, CategoryDto.category))
#         else:
#             return send_error(message='Category already exists')
#     except Exception as e:
#         return send_error(message=e)
#

# def get_list_category():
#     try:
#         list_category = Category.query.all()
#         return send_result(data=marshal(list_category, CategoryDto.category))
#     except Exception as e:
#         return send_error(message=e)
#
#
# def delete_category(data):
#     try:
#         category = Category.query.filter_by(categoryID=data['categoryID']).first()
#         if not category:
#             return send_error(message='Category not found')
#         else:
#             db.session.delete(category)
#             db.session.commit()
#             return send_result(message='Delete category successfully')
#     except Exception as e:
#         return send_error(message=e)
#
#
# def update_category(data):
#     try:
#         category = Category.query.filter_by(categoryID=data['categoryID']).first()
#         if not category:
#             return send_error(message='Category not found')
#         else:
#             category.categoryName = data['categoryName']
#             db.session.commit()
#             return send_result(message='Update category successfully')
#     except Exception as e:
#         return send_error(message=e)
