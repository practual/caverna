import React from 'react';


export default function Resources(props) {
    return (
        <ul>
            {Object.entries(props.resources).map(([resource, num], idx) => (
                <li key={idx}>{resource}: {num}</li>
            ))}
        </ul>
    );
}
