from models.game import get_all_types as db_all_types, get_all_modes as db_all_modes


def get_all_types():
    return [from_model_to_dict(_type) for _type in db_all_types()]


def get_all_modes():
    return [from_model_to_dict(_mode) for _mode in db_all_modes()]


def from_model_to_dict(game):
    return {'id': game.id,
            'name': game.name,
            'description': game.description}
