import React from 'react';

import Resources from '../resources';

import './action.css';


const Action = ({name, action, myMove, onSelect}) => (
    <div styleName="action" onClick={!action.dwarf && myMove ? onSelect : undefined}>
        <h3>{name}</h3>
        {action.resources && <Resources resources={action.resources} />}
        {action.dwarf && `(${action.dwarf.weapon})`}
    </div>
);

export default Action;
