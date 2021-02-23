import React, {useState} from 'react';

import Modal from '../modal';
import Action from './action';
import Expedition from './expedition';


const Logging1 = props => {
    const [isModalOpen, setIsModalOpen] = useState(props.action.dwarf?.progress >= 1);
    const [isExpeditionOpen, setIsExpeditionOpen] = useState(false);

    const openModal = () => {
        props.onSelect(props.action.id);
        setIsModalOpen(true);
    }
    const onSelectMaterial = () => {
        props.onSelect(props.action.id, {'mode': 'take_material'});
    };
    const onSelectExpedition = () => {
        setIsModalOpen(false);
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
            <Action name="Logging" {...props} onSelect={openModal} />
            {isModalOpen && (
                <Modal>
                    {takeMaterial}
                    '-- then / or --'
                    {expedition}
                </Modal>
            )}
            {isExpeditionOpen && (
                <Expedition
                    number={1}
                    weapon={props.action.dwarf.weapon}
                    onReturn={onExpeditionSelected}
                />
            )}
        </>
    );
};

export default Logging1;
