import React from 'react';
import {withRouter} from 'react-router';

import socket from '../socket';

const Player = withRouter(props => {
    const {gameId, playerId: myPlayerId} = props.match.params;

    const emitPlayerReady = () => {
        socket.emit('ready_player', gameId, myPlayerId);
    };

    let markReady;
    if (props.playerId === myPlayerId) {
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
