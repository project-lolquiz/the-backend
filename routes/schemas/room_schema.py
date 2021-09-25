post_schema = {
    'type': 'object',
    'properties': {
        'game_type': {'type': 'integer'},
        'game_mode': {'type': 'integer'},
        'host_user': {
            'type': 'object',
            'properties': {
                'uid': {'type': 'string'},
                'nickname': {'type': 'string'}
            },
            'required': ['uid', 'nickname']
        },
        'total_rounds': {'type': 'integer'},
    },
    'required': ['game_type', 'game_mode', 'total_rounds']
}

host_user_schema = {
    'type': 'object',
    'properties': {
        'uid': {'type': 'string'},
        'nickname': {'type': 'string'}
    },
    'required': ['uid', 'nickname']
}
