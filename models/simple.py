from app import get_db_connection

db = get_db_connection()


class Simple(db.Model):
    id = db.Column(db.BIGINT, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String, nullable=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Simple {}|{}>'.format(self.id, self.name)

    def add_new(self):
        db.session.add(self)
        db.session.commit()
