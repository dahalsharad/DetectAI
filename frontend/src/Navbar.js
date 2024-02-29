import React from 'react';
import "./App.css";
import Try from './Try';
import Check from './components/Check';
import { Link } from 'react-router-dom';

function Navbar() {


  return (
    <>
      <div className="navbar">
        <div className="aigon">
          <Link to="/" style={{ textDecoration: 'none' }}><p>DetectAI</p></Link>
        </div>
        <div className="about">
          <Link to="/about" style={{ textDecoration: 'none' }}>
            <p>
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
