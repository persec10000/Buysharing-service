from ..user.user import User
from app.app import db, flask_bcrypt
from ..common.model import Model
from datetime import date, time
import datetime


class History(Model):
    __tablename__ = "history"

    history_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)
    description = db.Column(db.Text)
    date_created = db.Column(db.Date)
    time_created = db.Column(db.Time)
    role = db.Column(db.String(45))

    def __init__(self, user_id, description=None, date_created=None, time_created=None, role=None):
        self.user_id = user_id
        self.description = description
        if date_created is None:
            date_created = date.today()
        self.date_created = date_created
        if time_created is None:
            time_created = datetime.datetime.now().time()
        self.time_created = time_created
        if role is None or str(role).strip().__eq__(''):
            role = 'user'
        self.role = role