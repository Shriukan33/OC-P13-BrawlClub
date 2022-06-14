import React from 'react'
import "./Nav.css"
import SearchBar from "./SearchBar"
import { Link } from 'react-router-dom'

const Nav = () => {
  return (
    <nav>
        <ul className="Logo">
            <li>
                <Link to="/"></Link>
            </li>
        </ul>
        <input id="menu-toggle" type="checkbox" />
        <label class='menu-button-container' for="menu-toggle">
            <div class='menu-button'></div>
        </label>
        <ul class="menu">
            <li>
                <Link to="/profile">Profile</Link>
            </li>
            <li>
                <Link to="/club">Club</Link>
            </li>
            <li>
                <Link to="leaderboard">Leaderboard</Link>
            </li>
        </ul>
        {/* <ul className="nav-elements">
            <li>
                <Link to="/profile">Profile</Link>
            </li>
            <li>
                <Link to="/club">Club</Link>
            </li>
            <li>
                <Link to="leaderboard">Leaderboard</Link>
            </li>
        </ul> */}
        <ul>
            <li>
                <SearchBar />
            </li>
        </ul>
    </nav>
  )
}

export default Nav