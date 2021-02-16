def find_player(players, player_id):
    for idx, player in enumerate(players):
        if player['id'] == player_id:
            return player, idx
