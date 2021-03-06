from datetime import datetime

from app import get_db_connection

db = get_db_connection()


def find_by_uid(uid):
    return User.query.filter_by(uid=uid)


def find_user_by_uid(uid):
    return find_by_uid(uid).first()


def update(user):
    find_by_uid(user['uid']) \
        .update({'nickname': user['nickname'],
                 'avatar_type': user['avatar']['type'],
                 'avatar_current_id': user['avatar']['current'],
                 'updated_at': datetime.now(),
                 'last_access': datetime.now()})
    db.session.commit()
    db.session.flush()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.BIGINT, primary_key=True, unique=True, nullable=False, autoincrement=True)
    uid = db.Column(db.String, nullable=False)
    nickname = db.Column(db.String, nullable=False)
    avatar_type = db.Column(db.String, nullable=True)
    avatar_current_id = db.Column(db.String, nullable=True)
    created_at = db.Column(db.TIMESTAMP, nullable=False, default=db.func.now())
    updated_at = db.Column(db.TIMESTAMP, nullable=False)
    last_access = db.Column(db.TIMESTAMP, nullable=True, default=db.func.now())

    def __init__(self, uid, nickname, avatar_type=None, avatar_current_id=None):
        self.uid = uid
        self.nickname = nickname
        self.avatar_type = avatar_type
        self.avatar_current_id = avatar_current_id
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.last_access = datetime.now()

    def __repr__(self):
        return '<User id={}|uid={}|nickname={}>'.format(self.id, self.uid, self.nickname)

    def add_new(self):
        db.session.add(self)
        db.session.commit()
        return self
