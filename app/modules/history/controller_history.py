from app.modules.common.controller import Controller
from .history import History
from app.app import db
from app.utils.geo import geo_distance
# import  datetime
from datetime import datetime, date, time


class ControllerHistory(Controller):
    def create(self, data):
        history = self._parse_history(data=data, history=None)
        db.session.add(history)
        db.session.commit()
        return history

    def get(self):
        histories = History.query.all()
        return histories

    def get_by_id(self, object_id):
        history = History.query.filter_by(history_id=object_id).first()
        return history

    def update(self, object_id, data):
        history = History.query.filter_by(history_id=object_id).first()
        if history is None:
            return False
        else:
            history = self._parse_history(data, history)
            db.session.commit()
            return history

    def delete(self, object_id):
        history = History.query.filter_by(history_id=object_id).first()
        if history is None:
            return False
        else:
            db.session.delete(history)
            db.session.commit()
            return True

    def get_last_history_user(self, user_id):
        histories = History.query.filter(user_id=user_id).order_by(History.date_created.desc()).order_by(
            History.time_created.desc())
        if histories is None or len(histories) == 0:
            return None
        first_hist = histories[0]
        return first_hist

    def _parse_history(self, data, history=None):
        user_id, description, date_created, time_created, role = None, None, None, None, None
        user_id = data['user_id']

        if 'description' in data:
            description = data['description']
        if 'date_created' in data:
            try:
                date_created = date.fromisoformat(data['date_created'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'time_created' in data:
            try:
                time_created = time.fromisoformat(data['time_created'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'role' in data:
            role = data['role']
        if history is None:
            history = History(user_id=user_id, description=description, date_created=date_created,
                              time_created=time_created, role=role)
        else:
            history.user_id = user_id
            history.description = description
            history.date_created = date_created
            history.time_created = time
            history.role = role
        return history
