from uuid import uuid4


class Player:
    @classmethod
    def deserialize(cls, state, logger):
        player = cls(logger, state['name'])
        player.player_id = state['id']
        player.ready = state['ready']
        player.resources = state['resources']
        player.board = Board.deserialize(state['board'], logger)
        return player

    def serialize(self):
        return {
            'id': self.player_id,
            'name': self.name,
            'ready': self.ready,
            'resources': self.resources,
            'board': self.board.serialize()
        }

    def __init__(self, logger, name):
        self.logger = logger
        self.name = name
        self.player_id = str(uuid4())
        self.ready = False
        self.resources = {}
        self.board = Board(self.logger)

    def toggle_ready(self):
        self.ready = not self.ready

    def add_resources(self, resources):
        for resource, num in resources.items():
            if not self.resources.get(resource):
                self.resources[resource] = 0
            self.resources[resource] += num


class Board:
    @classmethod
    def deserialize(cls, state, logger):
        board = cls(logger)
        board.tiles = state
        return board

    def serialize(self):
        return self.tiles

    def __init__(self, logger):
        self.logger = logger
        self.tiles = [{
            'coords': [(3, 3)],
            'type': 'dwelling',
            'name': 'Entry-level dwelling',
            'resources': {
                'dwarfs': [0, 0],
            },
        }, {
            'coords': [(2, 3)],
            'type' :'cavern',
        }]

    @property
    def num_dwarfs(self):
        return sum(len(tile.get('resources', {}).get('dwarfs', [])) for tile in self.tiles)
    
    def remove_smallest_dwarf(self):
        min_weapon = float('inf')
        tile_idx = -1
        for idx, tile in enumerate(self.tiles):
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
        dwarfs = []
        found_dwarf = False
        for dwarf in self.tiles[tile_idx]['resources']['dwarfs']:
            if not found_dwarf and dwarf == min_weapon:
                found_dwarf = True
                continue
            else:
                dwarfs.append(dwarf)
        self.tiles[tile_idx]['resources']['dwarfs'] = dwarfs
        return min_weapon
