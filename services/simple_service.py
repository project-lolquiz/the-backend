from models.simple import Simple


def get_all():
    return [{'id': simple.id, 'value': simple.name} for simple in Simple.query.all()]
