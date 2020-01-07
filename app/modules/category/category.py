from app.app import db
from app.modules.common.model import Model


class Category(Model):
    __tablename__ = "CATEGORY"

    categoryID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    categoryName = db.Column(db.String(50), nullable=False)
