import os

from flask import Flask, jsonify, render_template, request
from flask_socketio import SocketIO, emit

from cache import cache
from game import Game


app = Flask(__name__)
socketio = SocketIO(app, path='/api/socket.io')


def update_log(game_id, data):
    with open(os.path.join('./log', game_id), 'a+') as game_log:
        game_log.write(data + '\n')


@app.route('/<string:game_id>/<string:player_id>')
@app.route('/<string:game_id>')
@app.route('/')
def index(**kwargs):
    return render_template('index.html')


@app.route('/api/game', methods=['POST'])
def create_game():
    num_players = int(request.args.get('players', 1))
    game = Game(update_log)
    game.num_players = num_players
    game_state = game.serialize()
    update_log(game.game_id, 'CREATE GAME: {} players'.format(num_players))
    cache.set(game.game_id, game_state)
    return game.game_id, 201


@app.route('/api/game/<string:game_id>')
def get_game(game_id):
    return cache.get(game_id)


@socketio.on('add_player')
def add_player(game_id, name):
    game_state, cas = cache.gets(game_id)
    game = Game.deserialize(game_state, update_log)
    player = game.add_player(name)
    update_log(game_id, 'ADD PLAYER: {}, {}'.format(player.player_id, name))
    game_state = game.serialize()
    cache.cas(game_id, game_state, cas)
    emit('game_state', game_state, broadcast=True)
    return player.player_id


@socketio.on('ready_player')
def ready_player(game_id, player_id):
    update_log(game_id, 'READY PLAYER: {}'.format(player_id))
    game_state, cas = cache.gets(game_id)
    game = Game.deserialize(game_state, update_log)
    game.ready_player(player_id)
    game_state = game.serialize()
    cache.cas(game_id, game_state, cas)
    emit('game_state', game_state, broadcast=True)


@socketio.on('use_action')
def action(game_id, player_id, action_id, data):
    game_state, cas = cache.gets(game_id)
    game = Game.deserialize(game_state, update_log)
    game.use_action(action_id, data)
    game_state = game.serialize()
    cache.cas(game_id, game_state, cas)
    emit('game_state', game_state, broadcast=True)
    return True


if __name__ == '__main__':
    socketio.run(app)
