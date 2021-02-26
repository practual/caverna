import abc


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

    @property
    @abc.abstractmethod
    def action_id(self):
        pass

    @classmethod
    def deserialize(cls, state, logger):
        action_class = ACTION_MAP[state['id']]
        action = action_class(logger)
        action.resources = state['resources']
        action.dwarf = state['dwarf']
        return action

    def serialize(self):
        return {
            'id': self.action_id,
            'resources': self.resources,
            'dwarf': self.dwarf,
        }

    def __init__(self, logger):
        self.logger = logger
        self.resources = {}
        self.dwarf = {}


    def add_resources(self, game):
        if not self.resources:
            self.resources = {
                resource: quantity
                for resource, quantity in self.empty or self.topup
            }
        else:
            for resource, quantity in self.topup:
                self.resources[resource] = self.resources.get(resource, 0) + quantity

    def take_resources(self, player):
        player.add_resources(self.resources)
        self.resources = {}

    def process_use(self, game, player, data):
        if not data:
            # Default action, move dwarf to action.
            dwarf = player.board.remove_smallest_dwarf()
            self.dwarf = {'playerId': player.player_id, 'weapon': dwarf}

    def remove_dwarf(self):
        dwarf = self.dwarf
        self.dwarf = {}
        return dwarf


class Logging1(Action):
    action_id = LOGGING_1
    empty = [('wood', 3)]
    topup = [('wood', 1)]

    def process_use(self, game, player, data):
        super().process_use(game, player, data)
        if not data:
            self.dwarf['progress'] = 1
        elif data.get('mode') == 'take_material':
            self.take_resources(player)
            self.dwarf['progress'] = 2
            if not self.dwarf['weapon']:
                # Dwarf without a weapon cannot go on an expedition,
                # so reach terminal state here.
                return True


class WoodGathering(Action):
    action_id = WOOD_GATHERING
    topup = [('wood', 1)]

    def process_use(self, game, player, data):
        super().process_use(game, player, data)
        self.take_resources(player)
        return True


class Excavation1(Action):
    action_id = EXCAVATION_1
    topup = [('stone', 1)]


class OreMining1(Action):
    action_id = ORE_MINING_1
    empty = [('ore', 2)]
    topup = [('ore', 1)]


class Sustenance1(Action):
    action_id = SUSTENANCE_1
    topup = [('food', 1)]


class RubyMining(Action):
    action_id = RUBY_MINING

    topup = [('ruby', 1)]

    def add_resources(self, game):
        if game.num_players == 2 and game.turn < 3:
            return
        return super().add_resources(game)


class Housework(Action):
    action_id = HOUSEWORK


class SlashAndBurn(Action):
    action_id = SLASH_AND_BURN


class BlackSmithing(Action):
    action_id = BLACKSMITHING


class SheepFarming(Action):
    action_id = SHEEP_FARMING


class OreMineConstruction(Action):
    action_id = ORE_MINE_CONSTRUCTION


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
    SHEEP_FARMING: SheepFarming,
    ORE_MINE_CONSTRUCTION: OreMineConstruction,
}
