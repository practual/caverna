import React from 'react';
import ReactDOM from 'react-dom';
import {BrowserRouter, Switch, Route} from 'react-router-dom';

import Game from './game';
import Home from './home';

import './global.css';
import styles from './index.css';


const App = () => (
    <div styleName="styles.app-container">
        <BrowserRouter>
            <Switch>
                <Route path="/:gameId/:playerId?" component={Game} />
                <Route component={Home} />
            </Switch>
        </BrowserRouter>
    </div>
);

ReactDOM.render(<App/>, document.getElementById('app-mount'));
