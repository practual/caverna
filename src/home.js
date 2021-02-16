import React from 'react';

export default function Home(props) {
    function createGame() {
        fetch('/api/game', {method: 'POST'}).then(response => response.text()).then(gameId => {
            props.history.push(gameId);
        });
    }

    return <button onClick={createGame}>Create game</button>;
}
