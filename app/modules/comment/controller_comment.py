from app.app import db
from flask_restplus import marshal
import datetime

from app.modules.comment.comment import Comment
from app.modules.user.user import User

from app.utils.response import error, result
from app.modules.comment.dto_comment import DtoComment
from app.modules.common.controller import Controller


class ControllerComment(Controller):

    def create(self, data):
        try:
            comment = Comment(
                content=data['content'],
                rate=data['rate'],
                ordererID=data['ordererID'],
                shipperID=data['shipperID'],
                time=datetime.datetime.utcnow()
            )
            db.session.add(comment)
            db.session.commit()
            return result(message='Create comment successfully', data=marshal(comment, DtoComment.comment))
        except Exception as e:
            return error(message=e)

    def get(self):
        try:
            list_comment = Comment.query.all()
            list_comment = marshal(list_comment, DtoComment.comment)
            # shipper = User.query.filter_by(userID=data['userID']).first()
            for x in list_comment:
                shipper = User.query.filter_by(userID=x['shipperID']).first().name
                orderer = User.query.filter_by(userID=x['ordererID']).first().name
                x['shipperName'] = shipper
                x['ordererName'] = orderer
            return result(data=list_comment)
        except Exception as e:
            return error(message=e)

    def get_by_id(self, id):
        pass

    def update(self, data):
        pass

    def delete(self, data):
        try:
            comment = Comment.query.filter_by(commentID=data['commentID']).first()
            if not comment:
                return error(message='Comment not found')
            else:
                db.session.delete(comment)
                db.session.commit()
                return result(message='Delete comment successfully')
        except Exception as e:
            return error(message=e)

#
# def create_comment(data):
#     try:
#         comment = Comment(
#             content=data['content'],
#             rate=data['rate'],
#             ordererID=data['ordererID'],
#             shipperID=data['shipperID'],
#             time=datetime.datetime.utcnow()
#         )
#         db.session.add(comment)
#         db.session.commit()
#         return send_result(message='Create comment successfully', data=marshal(comment, CommentDto.comment))
#     except Exception as e:
#         return send_error(message=e)
#
#
# def get_list_comment():
#     try:
#         list_comment = Comment.query.all()
#         list_comment = marshal(list_comment, CommentDto.comment)
#         #shipper = User.query.filter_by(userID=data['userID']).first()
#         for x in list_comment:
#             shipper = User.query.filter_by(userID=x['shipperID']).first().name
#             orderer = User.query.filter_by(userID=x['ordererID']).first().name
#             x['shipperName'] = shipper
#             x['ordererName'] = orderer
#         return send_result(data=list_comment)
#     except Exception as e:
#         return send_error(message=e)
#
#
# def delete_comment(data):
#     try:
#         comment = Comment.query.filter_by(commentID=data['commentID']).first()
#         if not comment:
#             return send_error(message='Comment not found')
#         else:
#             db.session.delete(comment)
#             db.session.commit()
#             return send_result(message='Delete comment successfully')
#     except Exception as e:
#         return send_error(message=e)
