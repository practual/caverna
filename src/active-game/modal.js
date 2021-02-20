import React, {useEffect, useRef, useState} from 'react';
import ReactDOM from 'react-dom';

import './modal.css';


class ModalRegistry {
    constructor() {
        this.modals = [];
        this.listeners = [];
    }

    get activeModal() {
        return this.modals.length ? this.modals[0] : null;
    }

    addModal() {
        const id = Math.random().toString(16).substr(2);
        this.modals.push(id);
        for (const listener of this.listeners) {
            listener();
        }
        return id;
    }

    addListener(fn) {
        this.listeners.push(fn);
    }
}

const modalRegistry = new ModalRegistry();


export const ModalPortal = () => {
    const [isActive, setIsActive] = useState(false);
    useEffect(() => {
        modalRegistry.addListener(() => {
            setIsActive(!!modalRegistry.activeModal);
        });
    });
    const modalClass = isActive ? '' : 'closed';
    return (
        <>
            <div styleName={`modal-overlay ${modalClass}`}></div>
            <div styleName={`modal-container ${modalClass}`} id="modal-container"></div>
        </>
    );
};

const Modal = ({children}) => {
    const [id, setId] = useState(null);
    const [isActive, setIsActive] = useState(false);

    useEffect(() => {
        const modalId = modalRegistry.addModal();
        setId(modalId);
        setIsActive(modalRegistry.activeModal === modalId);
        modalRegistry.addListener(() => {
            setIsActive(modalRegistry.activeModal === id);
        });
    }, []);

    if (!isActive) {
        return null;
    }

    return ReactDOM.createPortal(
        <div styleName="modal">
            {children}
        </div>,
        document.getElementById('modal-container'),
    );
}

export default Modal;
