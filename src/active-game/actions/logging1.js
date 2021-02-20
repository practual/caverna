import React, {useState} from 'react';

import Modal from '../modal';
import Action from './action';


const Logging1 = props => {
    const [isModalOpen, setIsModalOpen] = useState(false);
    const openModal = () => {
        props.onSelect(props.id);
        setIsModalOpen(true);
    }
    const onSelect = () => {
        props.onSelect(props.id, {'mode': 'take_material'});
    };
    return (
        <>
            <Action name="Logging" {...props} onSelect={openModal} />
            {isModalOpen && (
                <Modal>
                    <a onClick={onSelect}>Take building materials</a>
                </Modal>
            )}
        </>
    );
};

export default Logging1;
