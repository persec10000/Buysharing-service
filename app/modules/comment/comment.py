from app.app import db
from app.modules.common.model import Model


class Comment(Model):
    __tablename__ = "COMMENT"

    commentID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(1000), nullable=False)
    rate = db.Column(db.Integer, nullable=False)
    ordererID = db.Column(db.Integer, db.ForeignKey('USER.userID'))
    shipperID = db.Column(db.Integer, db.ForeignKey('USER.userID'))
    time = db.Column(db.DateTime, nullable=False)
