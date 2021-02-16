import React, {useState} from 'react';

export default function Home(props) {
    const [numPlayers, setNumPlayers] = useState(1);
    function createGame() {
        const search = new URLSearchParams({players: numPlayers}).toString();
        fetch(`/api/game?${search}`, {method: 'POST'}).then(response => response.text()).then(gameId => {
            props.history.push(gameId);
        });
    }

    return (
        <div>
            <label>
                Number of players:
                <input type="number" value={numPlayers} onChange={ev => setNumPlayers(ev.target.value)} />
            </label>
            <button onClick={createGame}>Create game</button>
        </div>
    );
}
