import React, {useState} from 'react';

import Modal from '../modal';
import Action from './action';
import Expedition from './expedition';


const Logging1 = props => {
    const [isExpeditionOpen, setIsExpeditionOpen] = useState(false);
    let isModalOpen = !isExpeditionOpen && !!props.action.dwarf?.progress;
    if (props.action.dwarf?.progress > 1 && !props.action.dwarf.weapon) {
        isModalOpen = false;
    }

    const onSelectMaterial = () => {
        props.onSelect(props.action.id, {'mode': 'take_material'});
    };
    const onSelectExpedition = () => {
        setIsExpeditionOpen(true);
    };
    const onExpeditionSelected = () => {
        props.onSelect(props.action.id, {'mode': 'expedition'});
    };

    let takeMaterial = 'Take building materials';
    if (props.action.dwarf?.progress < 2) {
        takeMaterial = (
            <a onClick={onSelectMaterial}>{takeMaterial}</a>
        );
    }
    let expedition = 'Expedition (1)';
    if (props.action.dwarf?.weapon) {
        expedition = (
            <a onClick={onSelectExpedition}>{expedition}</a>
        );
    }
    return (
        <>
            <Action name="Logging" {...props} />
            {isModalOpen && (
                <Modal>
                    {takeMaterial}
                    '-- then / or --'
                    {expedition}
                </Modal>
            )}
            {isExpeditionOpen && (
                <Expedition
                    level={1}
                    weapon={props.action.dwarf.weapon}
                    onReturn={onExpeditionSelected}
                />
            )}
        </>
    );
};

export default Logging1;
