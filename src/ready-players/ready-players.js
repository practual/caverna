import PropTypes from 'prop-types';
import React, {useState} from 'react';
import {withRouter} from 'react-router';

import socket from '../socket';
import Player from './player';

const ReadyPlayers = withRouter((props) => {
    const gameId = props.match.params.gameId;
    const playerId = props.match.params.playerId;
    const [name, setName] = useState('');

    const addPlayer = () => {
        socket.emit('add_player', gameId, name, playerId => {
            props.history.push(`${gameId}/${playerId}`);
        });
    };

    return (
        <div>
            <div>
            <label>
                Your name:
                <input type="text" value={name} onChange={ev => setName(ev.target.value)} />
            </label>
            <button type="submit" onClick={addPlayer}>
                Join game
            </button>
            </div>
            <div>
                <h2>Players</h2>
                <ul>
                    {props.players.map(
                        player => <Player key={player.id} player={player} />
                    )}
                </ul>
            </div>
        </div>
    );
});
ReadyPlayers.propTypes = {
    players: PropTypes.array,
};
ReadyPlayers.defaultProps = {
    players: [],
};

export default ReadyPlayers;
