from models.simple import Simple


def add(content):
    new_simple = Simple(content['value'])
    new_simple.add_new()


def get_by_id(by_id):
    simple = Simple.query.filter_by(id=by_id).first_or_404()
    return from_model_to_dict(simple)


def get_all():
    return [from_model_to_dict(simple) for simple in Simple.query.all()]


def from_model_to_dict(simple):
    return {'id': simple.id, 'value': simple.name}
