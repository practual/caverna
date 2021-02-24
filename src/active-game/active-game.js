import React, {useState} from 'react';
import {withRouter} from 'react-router';

import socket from '../socket';
import Actions from './actions/actions';
import Board from './board';
import {ModalPortal} from './modal';
import Resources from './resources';

import './active-game.css';


const ActiveGame = withRouter(({game, match}) => {
    const {gameId, playerId} = match.params;
    const [focusPlayerId, setFocusPlayerId] = useState(playerId);
    const focusPlayer = game.players.find(player => player.id === focusPlayerId);
    const myMove = game.players[game.activePlayerIdx].id === playerId;

    const onSelect = (actionId, data) => {
        socket.emit('use_action', gameId, playerId, actionId, data);
    };

    return (
        <div styleName="game">
            <div styleName="column">
                <div>
                    {game.players.reduce((acc, player) => {
                        if (player.id === playerId) {
                            return acc;
                        }
                        acc.push(
                            <div key={player.id}>{player.name}</div>
                        )
                        return acc;
                    }, [])}
                </div>
                <div styleName="board-container">
                    <Board board={focusPlayer.board} />
                </div>
                <Resources resources={focusPlayer.resources} />
            </div>
            <div styleName="column">
                <Actions actions={game.actions} myMove={myMove} onSelect={onSelect} />
            </div>
            <ModalPortal />
        </div>
    );
});

export default ActiveGame;
