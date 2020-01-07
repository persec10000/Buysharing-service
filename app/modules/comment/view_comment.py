from flask import request
from flask_restplus import Resource

from app.modules.comment.dto_comment import DtoComment
from .controller_comment import ControllerComment # create_comment, get_list_comment, delete_comment
from app.modules.common.decorator import admin_token_required, token_required
# from app.modules.routing.route import Routing

# api = CommentDto.api
api = DtoComment.api
comment = DtoComment.model


@api.route('')
class CommentList(Resource):
    @admin_token_required
    def get(self):
        controllerComment = ControllerComment()
        return controllerComment.get() # get_list_comment()

    @token_required
    @api.expect(comment, validate=True)
    def post(self):
        data = request.json
        controllerComment = ControllerComment()
        return controllerComment.create(data) # create_comment(data)

    @token_required
    def delete(self):
        data = request.json
        controllerComment = ControllerComment()
        return controllerComment.delete(data) # delete_comment(data)