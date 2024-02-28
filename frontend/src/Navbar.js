import React, { useState } from 'react';
import "./App.css";
import Try from './Try';
import Check from './components/Check';
import { Link } from 'react-router-dom';

function Navbar() {
  const [aboutClicked, setAboutClicked] = useState(false);

  const handleAboutClick = () => {
    setAboutClicked(true);
  };

  return (
    <>
      <div className="navbar">
        <div className="aigon">
          <Link to="/" style={{ textDecoration: 'none' }}><p>DetectAI</p></Link>
        </div>
        <div className="about">
          <Link to="/about" style={{ textDecoration: 'none' }}>
            <p
              onClick={handleAboutClick}
              style={{ backgroundColor: aboutClicked ? '#AEFC06' : 'whitesmoke', color: aboutClicked ? 'white' : '#191919' }}
            >
              ABOUT
            </p>
          </Link>
        </div>
      </div>
      <Try />
      <Check />
    </>
  );
}

export default Navbar;
