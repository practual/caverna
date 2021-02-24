import React from 'react';

import Resources from '../resources';

import './action.css';


const Action = ({name, action, myMove, onSelect}) => {
    const onClick = () => onSelect(action.id);
    return (
        <div styleName="action" onClick={!action.dwarf.playerId && myMove ? onClick : undefined}>
            <h3>{name}</h3>
            {action.resources && <Resources resources={action.resources} />}
            {action.dwarf.playerId && `(${action.dwarf.weapon})`}
        </div>
    );
};

export default Action;
