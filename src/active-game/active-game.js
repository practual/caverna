import React, {useState} from 'react';
import {withRouter} from 'react-router';

import Board from './board';
import Resources from './resources';

import './active-game.css';


const ActiveGame = withRouter(({game, match}) => {
    const playerId = match.params.playerId;
    const [focusPlayerId, setFocusPlayerId] = useState(playerId);
    const focusPlayer = game.players.find(player => player.id === focusPlayerId);
    return (
        <div styleName="game">
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
            <div>
                Actions
                <ul>
                {game.actions.map(action => <li key={action}>{action}</li>)}
                </ul>
            </div>
        </div>
    );
});

export default ActiveGame;
