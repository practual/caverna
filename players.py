def find_player(players, player_id):
    for idx, player in enumerate(players):
        if player['id'] == player_id:
            return player, idx


def get_next_dwarf(player):
    min_weapon = float('inf')
    tile_idx = -1
    for idx, tile in enumerate(player['board']):
        resources = tile.get('resources')
        if not resources:
            continue
        dwarfs = resources.get('dwarfs')
        if not dwarfs:
            continue
        for dwarf in dwarfs:
            if dwarf < min_weapon:
                tile_idx = idx
                min_weapon = dwarf
    return tile_idx, min_weapon


def remove_dwarf_from_tile(player, tile_idx, weapon):
    new_dwarfs = []
    found_dwarf = False
    for dwarf in player['board'][tile_idx]['resources']['dwarfs']:
        if not found_dwarf and dwarf == weapon:
            found_dwarf = True
            continue
        new_dwarfs.append(weapon)
    player['board'][tile_idx]['resources']['dwarfs'] = new_dwarfs
