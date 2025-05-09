// ScrollButtons.js
import React from 'react';
import { FaArrowUp, FaArrowDown } from 'react-icons/fa';
import '../styles/ScrollButtons.css';

const ScrollButtons = () => {
  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const scrollToBottom = () => {
    window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
  };

  return (
    <div className="scroll-buttons">
      <button onClick={scrollToTop} className="scroll-btn up">
        <FaArrowUp />
      </button>
      <button onClick={scrollToBottom} className="scroll-btn down">
        <FaArrowDown />
      </button>
    </div>
  );
};

export default ScrollButtons;
