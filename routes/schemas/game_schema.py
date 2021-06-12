start_game_schema = {
    'type': 'object',
    'properties': {
        'users': {
            'type': 'array',
            'properties': {
                'uid': {'type': 'string'},
                'nickname': {'type': 'string'}
            },
            'required': ['uid', 'nickname']
        }
    },
    'required': ['users']
}