import React from 'react';

import Resources from '../resources';

import './action.css';


const Action = ({name, resources}) => (
    <div styleName="action">
        <h3>{name}</h3>
        {resources && <Resources resources={resources} />}
    </div>
);

export default Action;
