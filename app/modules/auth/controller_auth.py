from app.app import db

# from app.modules.user.user import User
# from app.modules.user.blacklist import BlacklistToken
from app.modules.user.user import User
from app.modules.user.blacklist import BlacklistToken
from app.modules.buying.buyer.buyer import Buyer
from app.modules.buying.supplier.supplier import Supplier
from app.modules.carpooling.driver.driver import Driver
from app.modules.carpooling.passenger.passenger import Passenger

from app.utils.response import error, result


def save_token(token):
    blacklist_token = BlacklistToken(token=token)
    try:
        # insert token
        db.session.add(blacklist_token)
        db.session.commit()
        return result(message='Successfully logged out.')
    except Exception as e:
        return error(message=e)


def get_id(user_id, role):
    if role == 'user':
        return None
    if role.__eq__('buyer'):
        buyer = Buyer.query.filter_by(user_id=user_id).order_by(Buyer.buyer_id.desc()).first()
        return buyer.buyer_id
    if role.__eq__('supplier'):
        supplier = Supplier.query.filter_by(user_id=user_id).order_by(Supplier.supplier_id.desc()).first()
        return supplier.supplier_id
    return None


class ControllerAuth:
    @staticmethod
    def login_user(data):
        try:
            user = User.query.filter_by(email=data.get('email')).first()
            if user and user.check_password(data.get('password')):
                auth_token = User.encode_auth_token(user.user_id)
                if user.blocked:
                    return None  # error(message='User has been blocked')
                if auth_token:
                    role = user.role
                    if role.__eq__('user'):
                        pass
                    if role.__eq__('buyer'):
                        buyer_id = get_id(user_id=user.user_id, role=role)
                        print("I am here",buyer_id)
                        user.buyer_id = buyer_id
                    if role.__eq__('supplier'):
                        supplier_id = get_id(user_id=user.user_id, role=role)
                        user.supplier_id = supplier_id
                    return user  # result(message='Successfully logged in', data={'Authorization': auth_token.decode()})
            else:
                return None  # error(message='Email or Password does not match')
        except Exception as e:
            return error(message=e)

    @staticmethod
    def logout_user(data):
        if data:
            auth_token = data.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                return save_token(token=auth_token)
            else:
                return error(message=resp)
        else:
            return error(message='Provide a valid auth token')

    @staticmethod
    def get_logged_user(new_request):
        auth_token = new_request.headers.get('Authorization')
        if auth_token:
            auth_token = auth_token.split(' ')[1]
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                user = User.query.filter_by(user_id=resp).first()
                return user  # tra lai JSON tương ứng về các roles đang thực hiện và các orders.
                # # print(user)
                # res = {
                #         'user_id': user.user_id,
                #         'email': user.email,
                #         'role': user.role,
                #         'name': user.name
                #         }
                # return result(data=res)
            return None  # error(message=resp)
        else:
            return None  # error(message='Provide a valid auth token')
