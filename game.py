import random


def start_game(state):
    random.shuffle(state['players'])
    num_players = state['numPlayers']
    state['startingPlayerIdx'] = 0
    for playerIdx in range(num_players):
        if playerIdx == 0:
            food = 1
        elif playerIdx == 1:
            food = 2
        else:
            food = 3
        if num_players == 1:
            food = 2
        state['players'][playerIdx]['resources'] = {
            'food': food,
        }
        state['players'][playerIdx]['board'] = [{
            'coords': [(3, 3)],
            'type': 'dwelling',
            'name': 'Entry-level dwelling',
            'resources': {
                'dwarfs': 2,
            },
        }]
    state['started'] = True
    return state
