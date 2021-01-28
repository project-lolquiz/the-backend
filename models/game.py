from app import get_db_connection

db = get_db_connection()


def get_all_types():
    return GameType.query.all()


class GameType(db.Model):
    __tablename__ = 'game_types'
    id = db.Column(db.BIGINT, primary_key=True, unique=True, nullable=False, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    created_at = db.Column(db.TIMESTAMP, nullable=False, default=db.func.now())
    updated_at = db.Column(db.TIMESTAMP, nullable=False, default=db.func.now())

    def __init__(self):
        pass

    def __init__(self, _id, name, description):
        self.id = _id
        self.name = name
        self.description = description

    def __repr__(self):
        return '<GameType id={}|name={}|description={}>'.format(self.id, self.name, self.description)


def get_all_modes():
    return GameMode.query.all()


class GameMode(db.Model):
    __tablename__ = 'game_modes'
    id = db.Column(db.BIGINT, primary_key=True, unique=True, nullable=False, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    created_at = db.Column(db.TIMESTAMP, nullable=False, default=db.func.now())
    updated_at = db.Column(db.TIMESTAMP, nullable=False, default=db.func.now())

    def __init__(self):
        pass

    def __init__(self, _id, name, description):
        self.id = _id
        self.name = name
        self.description = description

    def __repr__(self):
        return '<GameMode id={}|name={}|description={}>'.format(self.id, self.name, self.description)
