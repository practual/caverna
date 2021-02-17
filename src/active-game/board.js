import React, {useCallback, useState} from 'react';

import './board.css';


export default function Board(props) {
    const aspectRatio = 6 / 4;
    const [boardDimensions, setBoardDimensions] = useState({});
    const ref = useCallback(el => {
        if (!el) {
            return;
        }
        const ro = new ResizeObserver(([entry]) => {
            const {height, width} = entry.contentRect;
            if (width / height > aspectRatio) {
                setBoardDimensions({width: height * aspectRatio, height});
            } else {
                setBoardDimensions({width, height: width / aspectRatio});
            }
        })
        ro.observe(el);
    }, []);

    return (
        <div ref={ref} styleName="board-container">
            <div styleName="board" style={boardDimensions}>
            </div>
        </div>
    );
}
