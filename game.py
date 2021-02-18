import random

import actions as act

def get_starting_actions(num_players):
    actions = []
    if num_players == 3:
        actions.extend((
            act.STRIP_MINING,
            act.IMITATION_1,
            act.FOREST_EXPLORATION_1,
        ))
    if num_players == 7:
        actions.extend((
            act.LARGE_DEPOT,
            act.IMITATION_2,
            act.EXTENSION,
        ))
    if num_players == 5:
        actions.extend((
            act.DEPOT,
            act.WEEKLY_MARKET,
            act.HARDWARE_RENTAL_1,
            act.SMALL_SCALE_DRIFT_MINING,
            act.IMITATION_1,
            act.FENCE_BUILDING_1,
        ))
    if num_players >= 6:
        actions.extend((
            act.DEPOT,
            act.WEEKLY_MARKET,
            act.HARDWARE_RENTAL_2,
            act.DRIFT_MINING_1,
            act.IMITATION_3,
            act.FENCE_BUILDING_2,
        ))
    if num_players == 1:
        actions.extend((
            act.LOGGING_1,
            act.WOOD_GATHERING,
            act.EXCAVATION_1,
            act.ORE_MINING_1,
            act.SUSTENANCE_1,
        ))
    elif num_players <= 3:
        actions.extend((
            act.DRIFT_MINING_1,
            act.LOGGING_1,
            act.WOOD_GATHERING,
            act.EXCAVATION_1,
            act.SUPPLIES,
            act.CLEARING_1,
            act.STARTING_PLAYER_1,
            act.ORE_MINING_1,
            act.SUSTENANCE_1,
        ))
    else:
        actions.extend((
            act.DRIFT_MINING_2,
            act.IMITATION_4,
            act.LOGGING_2,
            act.FOREST_EXPLORATION_2,
            act.EXCAVATION_2,
            act.GROWTH,
            act.CLEARING_2,
            act.STARTING_PLAYER_2,
            act.ORE_MINING_2,
            act.SUSTENANCE_2,
        ))
    actions.extend((
        act.RUBY_MINING,
        act.HOUSEWORK,
        act.SLASH_AND_BURN,
    ))
    return actions

def get_action_for_turn(num_players, turn_num, actions):
    if num_players < 3 and turn_num == 8:
        raise Exception('No turn 9 for 1 or 2 player games')
    if num_players == 1:
        solo_actions = act.STAGE_1_ACTIONS + act.STAGE_2_ACTIONS + act.STAGE_3_ACTIONS + act.STAGE_4_ACTIONS
        return solo_actions[turn_num]
    if turn_num <= 2:
        stage_actions = act.STAGE_1_ACTIONS,
    elif turn_num <= 5:
        stage_actions = act.STAGE_2_ACTIONS,
    elif turn_num <= 8:
        stage_actions = act.STAGE_3_ACTIONS,
    else:
        stage_actions = act.STAGE_4_ACTIONS
    remaining_actions = list(set(stage_actions) - set(actions))
    return random.shuffle(remaining_actions)[0]


def start_game(state):
    random.shuffle(state['players'])
    state['turn'] = 0
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
