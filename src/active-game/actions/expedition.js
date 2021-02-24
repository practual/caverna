import React, {useState} from 'react';

import Modal from '../modal';


const Expedition = ({level}) => {
    const [selectedResources, setSelectedResources] = useState({});
    const itemsRemaining = level - Object.values(selectedResources).reduce((acc, el) => acc + el, 0);
    return (
        <Modal>
            {`Choose your loot! ${itemsRemaining} items remaining.`}
        </Modal>
    );
};

export default Expedition;
