import React from "react";
import "./Nav.css";
import { Link } from "react-router-dom";

const Nav = () => {
  return (
    <nav>
      <div className="d-flex align-items-center">
        <Link to="/">
          <img src="/images/brawlclub_logo.png" alt="logo" width="62px" />
        </Link>
      </div>

      <div className="d-flex ">
        <input id="menu-toggle" type="checkbox" />
        <label className="menu-button-container" htmlFor="menu-toggle">
          <div className="menu-button"></div>
        </label>

        <ul className="menu">
          <li>
            <Link to="/club-finder">Club Finder</Link>
          </li>
          <li>
            <Link to="leaderboard/players">Leaderboards</Link>
          </li>
        </ul>
      </div>
    </nav>
  );
};

export default Nav;
