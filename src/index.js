import React from 'react';
import ReactDOM from 'react-dom';
import {BrowserRouter, Switch, Route} from 'react-router-dom';

import Game from './game';
import Home from './home';


const App = () => (
    <BrowserRouter>
        <Switch>
            <Route path="/:gameId/:playerId?" component={Game} />
            <Route component={Home} />
        </Switch>
    </BrowserRouter>
);

ReactDOM.render(<App/>, document.getElementById('app-mount'));
