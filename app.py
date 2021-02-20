import os
from uuid import uuid4

from flask import Flask, jsonify, render_template, request
from flask_socketio import SocketIO, emit

from cache import cache
from game import get_action_for_turn, get_starting_actions, start_game, start_turn
from players import find_player


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
    game_id = str(uuid4())
    num_players = int(request.args.get('players', 1))
    update_log(game_id, 'CREATE GAME: {} players'.format(num_players))
    game_state = {
        'id': game_id,
        'numPlayers': num_players,
        'started': False,
        'actions': get_starting_actions(num_players),
    }
    cache.set(game_id, game_state)
    return game_id, 201

@app.route('/api/game/<string:game_id>')
def get_game(game_id):
    return cache.get(game_id)

@socketio.on('add_player')
def add_player(game_id, name):
    player_id = str(uuid4())
    update_log(game_id, 'ADD PLAYER: {}, {}'.format(player_id, name))
    game_state, cas = cache.gets(game_id)
    if 'players' not in game_state:
        game_state['players'] = []
    game_state['players'].append({'id': player_id, 'name': name, 'ready': False})
    cache.cas(game_id, game_state, cas)
    emit('game_state', game_state, broadcast=True)
    return player_id

@socketio.on('ready_player')
def ready_player(game_id, player_id):
    update_log(game_id, 'READY PLAYER: {}'.format(player_id))
    game_state, cas = cache.gets(game_id)
    player, idx = find_player(game_state['players'], player_id)
    player['ready'] = not player['ready']
    game_state['players'][idx] = player
    num_ready = sum(player['ready'] for player in game_state['players'])
    if num_ready == game_state['numPlayers']:
        game_state = start_game(game_state)
        game_state, log_msg = start_turn(game_state)
        update_log(game_id, log_msg)
    cache.cas(game_id, game_state, cas)
    emit('game_state', game_state, broadcast=True)

@socketio.on('connect')
def test_connect():
    emit('my_response', {'data': 'Connected'})

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app)
