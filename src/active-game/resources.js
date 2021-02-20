import React from 'react';


export default function Resources(props) {
    return (
        <ul>
            {Object.entries(props.resources).map(([resource, num], idx) => {
                if (resource == 'dwarfs') {
                    num = num.map(weapon => `(${weapon})`).join(', ');
                }
                return <li key={idx}>{resource}: {num}</li>;
            })}
        </ul>
    );
}
