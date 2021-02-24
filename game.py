import random
from uuid import uuid4

import actions as act
from actions import Action
from players import Player


class Game:
    @classmethod
    def deserialize(cls, state, logger):
        game = cls(logger)
        game.game_id = state['id']
        game.num_players = state['numPlayers']
        for player in state['players']:
            game.players.append(Player.deserialize(player, logger))
        for action in state['actions']:
            game.actions.append(Action.deserialize(action, logger))
        game.turn = state['turn']
        game.starting_player_idx = state['startingPlayerIdx']
        game.active_player_idx = state['activePlayerIdx']
        return game

    def serialize(self):
        return {
            'id': self.game_id,
            'numPlayers': self.num_players,
            'players': [player.serialize() for player in self.players],
            'actions': [action.serialize() for action in self.actions],
            'turn': self.turn,
            'startingPlayerIdx': self.starting_player_idx,
            'activePlayerIdx': self.active_player_idx,
        }

    def __init__(self, logger):
        super().__init__()
        self.logger = logger
        self.game_id = str(uuid4())
        self.num_players = 1
        self.players = []
        self.actions = []
        self.turn = -1
        self.starting_player_idx = 0
        self.active_player_idx = 0

    def add_player(self, name):
        player = Player(self.logger, name)
        self.players.append(player)
        return player

    def ready_player(self, player_id):
        player = self._get_player_by_id(player_id)
        player.toggle_ready()
        for player in self.players:
            if not player.ready:
                return
        self.start_game()

    def start_game(self):
        random.shuffle(self.players)
        for idx, player in enumerate(self.players):
            if idx == 0 or idx == 1:
                food = 1
            elif idx == 2:
                food = 2
            else:
                food = 3
            if self.num_players == 1:
                food = 2
            player.add_resources({'food': food})
        self.actions = self._get_starting_actions()
        self.advance_turn()

    def advance_turn(self):
        self.turn += 1
        self.actions.append(self._get_action_for_turn())
        for action in self.actions:
            action.add_resources(self)
        self.active_player_idx = self.starting_player_idx

    def use_action(self, action_id, data):
        player = self.players[self.active_player_idx]
        action = self._get_action_by_id(action_id)
        if action.process_use(self, player, data):
            # All action modes used
            self.pass_priority()

    def pass_priority(self):
        def _advance_priority(num_passes):
            return self.players[(self.active_player_idx + num_passes) % self.num_players]
        p = 1
        player = _advance_priority(p)
        while not player.board.num_dwarfs:
            p += 1
            if p > self.num_players:
                return self.harvest()
            player = _advance_priority(p)
        self.active_player_idx = (self.active_player_idx + p) % self.num_players

    def harvest(self):
        pass

    def _get_player_by_id(self, player_id):
        for player in self.players:
            if player.player_id == player_id:
                return player

    def _get_action_by_id(self, action_id):
        for action in self.actions:
            if action.action_id == action_id:
                return action

    def _get_starting_actions(self):
        actions = []
        if self.num_players == 3:
            actions.extend((
                act.STRIP_MINING,
                act.IMITATION_1,
                act.FOREST_EXPLORATION_1,
            ))
        if self.num_players == 7:
            actions.extend((
                act.LARGE_DEPOT,
                act.IMITATION_2,
                act.EXTENSION,
            ))
        if self.num_players == 5:
            actions.extend((
                act.DEPOT,
                act.WEEKLY_MARKET,
                act.HARDWARE_RENTAL_1,
                act.SMALL_SCALE_DRIFT_MINING,
                act.IMITATION_1,
                act.FENCE_BUILDING_1,
            ))
        if self.num_players >= 6:
            actions.extend((
                act.DEPOT,
                act.WEEKLY_MARKET,
                act.HARDWARE_RENTAL_2,
                act.DRIFT_MINING_1,
                act.IMITATION_3,
                act.FENCE_BUILDING_2,
            ))
        if self.num_players == 1:
            actions.extend((
                act.LOGGING_1,
                act.WOOD_GATHERING,
                act.EXCAVATION_1,
                act.ORE_MINING_1,
                act.SUSTENANCE_1,
            ))
        elif self.num_players <= 3:
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
        action_objs = []
        for action_id in actions:
            action_cls = act.ACTION_MAP[action_id]
            action_objs.append(action_cls(self.logger))
        return action_objs

    def _get_action_for_turn(self):
        if self.num_players < 3 and self.turn == 8:
            raise Exception('No turn 9 for 1 or 2 player games')
        if self.num_players == 1:
            solo_actions = (
                act.STAGE_1_ACTIONS +
                act.STAGE_2_ACTIONS +
                act.STAGE_3_ACTIONS +
                act.STAGE_4_ACTIONS
            )
            return act.ACTION_MAP[solo_actions[self.turn]](self.logger)
        if self.turn <= 2:
            stage_actions = act.STAGE_1_ACTIONS
        elif self.turn <= 5:
            stage_actions = act.STAGE_2_ACTIONS
        elif self.turn <= 8:
            stage_actions = act.STAGE_3_ACTIONS
        else:
            stage_actions = act.STAGE_4_ACTIONS
        remaining_actions = list(set(stage_actions) - set(action.action_id for action in self.actions))
        random.shuffle(remaining_actions)
        return act.ACTION_MAP[remaining_actions[0]](self.logger)
