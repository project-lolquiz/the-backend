def get_current_players(current_room):
    host_user = current_room['host_user']
    users = current_room['game']['users']
    players = [player for player in users]
    players.append(host_user)
    return players
