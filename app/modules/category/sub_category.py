from app.app import db
from app.modules.common.model import Model


class SubCategory(Model):
    __tablename__ = 'SUB_CATEGORY'

    subCategooryID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subCategoryName = db.Column(db.String(50), nullable=False)
    categoryID = db.Column(db.Integer, db.ForeignKey('CATEGORY.categoryID'), nullable=False)
    category = db.relationship('Category', backref=db.backref('SUB_CATEGORY', lazy=True))