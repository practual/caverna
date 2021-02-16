import React, {useEffect, useState} from 'react';

import ReadyPlayers from './ready-players/ready-players';
import socket from './socket';

export default function Game(props) {
    const [isLoading, setIsLoading] = useState(true);
    const [gameState, setGameState] = useState({});

    useEffect(() => {
        if (!isLoading) {
            return;
        }
        fetch(`/api/game/${props.match.params.gameId}`).then(response => response.json()).then(response => {
            setGameState(response);
            setIsLoading(false);
        });
    }, [isLoading]);

    useEffect(() => {
        socket.on('game_state', setGameState);
        return () => {
            socket.off('game_state', setGameState);
        };
    });

    if (isLoading) {
        return null;
    }

    return <ReadyPlayers players={gameState.players} />;
}
