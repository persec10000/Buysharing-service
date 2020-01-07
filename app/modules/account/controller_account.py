from ..common.controller import Controller
from .account import Account

from app.app import db


class ControllerAccount(Controller):
    def create(self, data):
        account = self._parse_account(data=data, account=None)
        db.session.add(account)
        db.session.commit()

    def get(self):
        accounts = Account.query.all()
        return accounts

    def get_by_id(self, object_id):
        account = Account.query.filter_by(account_id=object_id).first()
        return account

    def update(self, object_id, data):
        account = self.get_by_id(object_id=object_id)
        if account is None:
            return False
        account = self._parse_account(data=data, account=account)
        db.session.commit()

    def delete(self, object_id):
        account = self.get_by_id(object_id=object_id)
        db.session.delete(account)
        db.session.commit()

    def _parse_account(self, data, account=None):
        user_id, account_name, account_number, balance, date_created, card_number, card_type, card_expired_date, card_security_number, bank_name, bank_swift, card_holder_name = None, None, None, None, None, None, None, None, None, None, None, None
        user_id = data['user_id']
        if 'account_name' in data:
            account_name = data['account_name']
        if 'account_number' in data:
            account_number = data['account_number']
        if 'balance' in data:
            balance = data['balance']
        if 'date_created' in data:
            date_created = data['date_created']
        if 'card_number' in data:
            card_number = data['card_number']
        if 'card_type' in data:
            card_type = data['card_type']
        if 'card_expired_date' in data:
            card_expired_date = data['card_expired_date']
        if 'card_security_number' in data:
            card_security_number = data['card_security_number']
        if 'bank_name' in data:
            bank_name = data['bank_name']
        if 'bank_swift' in data:
            bank_swift = data['bank_swift']
        if 'card_holder_name' in data:
            card_holder_name = data['card_holder_name']

        if account is None:
            account = Account(user_id=user_id, account_name=account_name, account_number=account_number,
                              balance=balance, date_created=date_created, card_number=card_number, card_type=card_type,
                              card_expired_date=card_expired_date, card_security_number=card_security_number,
                              bank_name=bank_name, bank_swift=bank_swift, card_holder_name=card_holder_name)
        else:
            account.user_id = user_id
            account.account_name = account_name
            account.account_number = account_number
            account.balance = balance
            account.date_created = date_created
            account.card_number = card_number
            account.card_type = card_type
            account.card_expired_date = card_expired_date
            account.card_security_number = card_security_number
            account.bank_name = bank_name
            account.bank_swift = bank_swift
            account.card_holder_name = card_holder_name
        return account
