game_answer_schema = {
    'type': 'object',
    'properties': {
        'selected_user_id': {'type': 'string'},
        'users': {
            'type': 'array',
            'items': {
                'properties': {
                    'uid': {'type': 'string'},
                    'chosen_answer': {'type': ['string', 'null']}
                },
                'required': ['uid', 'chosen_answer']
            }
        }
    },
    'required': ['selected_user_id', 'users']
}
