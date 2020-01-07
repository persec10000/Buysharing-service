from app.app import db, flask_bcrypt
from ..common.model import Model


class Account(Model):
    __tablename__ = "account"

    account_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # relationship
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    user = db.relationship('User', backref=db.backref('accounts', lazy=True))

    account_name = db.Column(db.String(45))
    account_number = db.Column(db.String(45))
    balance = db.Column(db.Float)

    date_created = db.Column(db.Date)
    card_number = db.Column(db.String(45))
    card_type = db.Column(db.String(45))

    card_expired_date = db.Column(db.Date)
    card_security_number = db.Column(db.String(45))

    bank_name = db.Column(db.String(255))
    bank_swift = db.Column(db.String(255))
    card_holder_name = db.Column(db.String(80))

    def __init__(self, user_id, account_name=None, account_number=None, balance=None, date_created=None,
                 card_number=None, card_type=None, card_expired_date=None, card_security_number=None, bank_name=None,
                 bank_swift=None, card_holder_name=None):
        self.user_id = user_id
        self.account_name = account_name
        self.account_number = account_number
        self.balance = balance

        self.date_created = date_created
        self.card_number = card_number
        self.card_type = card_type

        self.card_expired_date = card_expired_date
        self.card_security_number = card_security_number

        self.bank_name = bank_name
        self.bank_swift = bank_swift
        self.card_holder_name = card_holder_name

    def __repr__(self):
        pass
