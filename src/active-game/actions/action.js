import React from 'react';

import Resources from '../resources';

import './action.css';


const Action = ({name, resources, dwarf, myMove, onSelect}) => (
    <div styleName="action" onClick={!dwarf && myMove ? onSelect : undefined}>
        <h3>{name}</h3>
        {resources && <Resources resources={resources} />}
        {dwarf && `(${dwarf.weapon})`}
    </div>
);

export default Action;
