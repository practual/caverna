import React from 'react';

import Blacksmithing from './blacksmithing';
import {ACTIONS} from './constants';
import Excavation1 from './excavation1';
import Housework from './housework';
import Logging1 from './logging1';
import OreMining1 from './ore-mining1';
import RubyMining from './ruby-mining';
import SlashAndBurn from './slash-and-burn';
import Sustenance1 from './sustenance1';
import WoodGathering from './wood-gathering';

import './actions.css';


const ACTION_MAP = Object.freeze({
   [ACTIONS.LOGGING_1]: Logging1, 
   [ACTIONS.WOOD_GATHERING]: WoodGathering,
   [ACTIONS.EXCAVATION_1]: Excavation1,
   [ACTIONS.ORE_MINING_1]: OreMining1,
   [ACTIONS.SUSTENANCE_1]: Sustenance1,
   [ACTIONS.RUBY_MINING]: RubyMining,
   [ACTIONS.HOUSEWORK]: Housework,
   [ACTIONS.SLASH_AND_BURN]: SlashAndBurn,
   [ACTIONS.BLACKSMITHING]: Blacksmithing,
});


const Actions = ({actions}) => (
    <div styleName="actions">
        {actions.map(actionId => {
            const ActionComponent = ACTION_MAP[actionId];
            return <ActionComponent key={actionId} />;
        })}
    </div>
);

export default Actions;
