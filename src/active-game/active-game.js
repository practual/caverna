import React, {useState} from 'react';
import {withRouter} from 'react-router';

import Resources from './resources';

import './active-game.css';


const ActiveGame = withRouter(({game, match}) => {
    const playerId = match.params.playerId;
    const [focusPlayerId, setFocusPlayerId] = useState(playerId);
    const focusPlayer = game.players.find(player => player.id === focusPlayerId);
    return (
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
            <div>
                <div styleName="board">
                    <div styleName="tile"></div>
                </div>
                <Resources resources={focusPlayer.resources} />
            </div>
        </div>
    );
});

export default ActiveGame;
