import React from 'react';
import {withRouter} from 'react-router';

import socket from '../socket';

const Player = withRouter(props => {
    const {gameId, playerId} = props.match.params;

    const emitPlayerReady = () => {
        socket.emit('ready_player', gameId, playerId);
    };

    let markReady;
    if (props.player.id === playerId) {
        markReady = (
            <button onClick={emitPlayerReady}>
                {props.player.ready ? 'Not Ready' : 'Ready'}
            </button>
        );
    }

    return (
        <li>
            {props.player.name}{' - '}
            {props.player.ready ? 'Ready' : 'Not Ready'}
            {markReady}
        </li>
    );
});

export default Player;
