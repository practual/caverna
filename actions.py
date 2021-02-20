import abc

from players import get_next_dwarf, remove_dwarf_from_tile


DRIFT_MINING_1 = 'drift_mining_1'
EXCAVATION_1 = 'excavation_1'
STARTING_PLAYER_1 = 'starting_player_1'
LOGGING_1 = 'logging_1'
SUPPLIES = 'supplies'
ORE_MINING_1 = 'ore_mining_1'
WOOD_GATHERING = 'wood_gathering'
CLEARING_1 = 'clearing_1'
SUSTENANCE_1 = 'sustenance_1'
DRIFT_MINING_2 = 'drift_mining_2'
EXCAVATION_2 = 'excavation_2'
STARTING_PLAYER_2 = 'starting_player_2'
IMITATION_1 = 'imitation_1'
LOGGING_2 = 'logging_2'
GROWTH = 'growth'
ORE_MINING_2 = 'ore_mining_2'
FOREST_EXPLORATION_1 = 'forest_exploration_1'
CLEARING_2 = 'clearing_2'
SUSTENANCE_2 = 'sustenance_2'
DEPOT = 'depot'
SMALL_SCALE_DRIFT_MINING = 'small_scale_drift_mining'
WEEKLY_MARKET = 'weekly_market'
IMITATION_2 = 'imitation_2'
HARDWARE_RENTAL_1 = 'hardware_rental_1'
FENCE_BUILDING_1 = 'fence_building_1'
IMITATION_3 = 'imitation_3'
HARDWARE_RENTAL_2 = 'hardware_rental_2'
FENCE_BUILDING_2 = 'fence_building_2'
RUBY_MINING = 'ruby_mining'
HOUSEWORK = 'housework'
SLASH_AND_BURN = 'slash_and_burn'
STRIP_MINING = 'strip_mining'
IMITATION_4 = 'imitation_4'
FOREST_EXPLORATION_2 = 'forest_exploration_2'
LARGE_DEPOT = 'large_depot'
EXTENSION = 'extension'
SHEEP_FARMING = 'sheep_farming'
BLACKSMITHING = 'blacksmithing'
ORE_MINE_CONSTRUCTION = 'ore_mine_construction'
WISH_FOR_CHILDREN = 'wish_for_children'
URGENT_WISH_FOR_CHILDREN = 'urgent_wish_for_children'
DONKEY_FARMING = 'donkey_farming'
RUBY_MINE_CONSTRUCTION = 'ruby_mine_construction'
FAMILY_LIFE = 'family_life'
ORE_DELIVERY = 'ore_delivery'
EXPLORATION = 'exploration'
RUBY_DELIVERY = 'ruby_delivery'
ORE_TRADING = 'ore_trading'
ADVENTURE = 'adventure'

STAGE_1_ACTIONS = [
    BLACKSMITHING,
    SHEEP_FARMING,
    ORE_MINE_CONSTRUCTION,
]

STAGE_2_ACTIONS = [
    WISH_FOR_CHILDREN,
    DONKEY_FARMING,
    RUBY_MINE_CONSTRUCTION,
]

STAGE_3_ACTIONS = [
    ORE_DELIVERY,
    FAMILY_LIFE,
    EXPLORATION,
]

STAGE_4_ACTIONS = [
    ORE_TRADING,
    ADVENTURE,
    RUBY_DELIVERY,
]


class Action(metaclass=abc.ABCMeta):
    empty = []
    topup = []


    def __init__(self, state):
        self.state = state


    def add_resources(self, current_resources):
        if not current_resources:
            return {
                resource: quantity
                for resource, quantity in self.empty or self.topup
            }
        return {
            resource: current_resources.get(resource, 0) + quantity
            for resource, quantity in self.topup
        }

    def process_use(self, player, action, data):
        if not data:
            # Default action, move dwarf to action.
            tile_idx, dwarf = get_next_dwarf(player)
            remove_dwarf_from_tile(player, tile_idx, dwarf)
            action['dwarf'] = {'playerId': player['id'], 'weapon': dwarf}


class Logging1(Action):
    empty = [('wood', 3)]
    topup = [('wood', 1)]

    def process_use(self, player, action, data):
        super().process_use(player, action, data)


class WoodGathering(Action):
    topup = [('wood', 1)]


class Excavation1(Action):
    topup = [('stone', 1)]


class OreMining1(Action):
    empty = [('ore', 2)]
    topup = [('ore', 1)]


class Sustenance1(Action):
    topup = [('food', 1)]


class RubyMining(Action):
    @property
    def topup(self):
        if self.state['numPlayers'] == 2 and state['turn'] < 3:
            return []
        return [('ruby', 1)]


class Housework(Action):
    pass    


class SlashAndBurn(Action):
    pass


class BlackSmithing(Action):
    pass


ACTION_MAP = {
    LOGGING_1: Logging1,
    WOOD_GATHERING: WoodGathering,
    EXCAVATION_1: Excavation1,
    ORE_MINING_1: OreMining1,
    SUSTENANCE_1: Sustenance1,
    RUBY_MINING: RubyMining,
    HOUSEWORK: Housework,
    SLASH_AND_BURN: SlashAndBurn,
    BLACKSMITHING: BlackSmithing,
}


def find_action(actions, action_id):
    for idx, action in enumerate(actions):
        if action['id'] == action_id:
            return action, idx


def add_resources(state):
    updated_actions = []
    for action in state['actions']:
        action_obj = ACTION_MAP[action['id']](state)
        updated_actions.append({
            'id': action['id'],
            'resources': action_obj.add_resources(action['resources'])
        })
    state['actions'] = updated_actions
    return state
