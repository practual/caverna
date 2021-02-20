import React, {useCallback, useState} from 'react';

import Resources from './resources';

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
                {props.board.map(tile => {
                    let minX = Infinity, minY = Infinity, maxX = 0, maxY = 0;
                    for (const [x, y] of tile.coords) {
                        minX = Math.min(minX, x);
                        maxX = Math.max(maxX, x);
                        minY = Math.min(minY, y);
                        maxY = Math.max(maxY, y);
                    }
                    const gridArea = `${minX + 1} / ${minY + 1} / ${maxX + 1} / ${maxY + 1}`;
                    return (
                        <div key={tile.coords} style={{gridArea}} styleName={`tile--${tile.type}`}>
                            {tile.name}
                            {tile.resources && <Resources resources={tile.resources} />}
                        </div>
                    );
                })}
            </div>
        </div>
    );
}
