post_schema = {
    'type': 'object',
    'properties': {
        'uid': {'type': 'string'},
        'nickname': {'type': 'string'},
        'avatar': {
            'type': 'object',
            'properties': {
                'type': {'type': 'string'},
                'current': {'type': 'string'}
            }
        }
    },
    'required': ['uid', 'nickname']
}


put_schema = {
    'type': 'object',
    'properties': {
        'nickname': {'type': 'string'},
        'avatar': {
            'type': 'object',
            'properties': {
                'type': {'type': 'string'},
                'current': {'type': 'string'}
            },
            'required': ['type', 'current']
        }
    },
    'required': ['nickname', 'avatar']
}


put_avatar_schema = {
    'type': 'object',
    'properties': {
        'type': {'type': 'string'},
        'current': {'type': 'string'}
    },
    'required': ['type', 'current']
}