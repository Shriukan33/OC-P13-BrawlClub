import React from 'react'
import "./Nav.css"
import SearchBar from "./SearchBar"
import { Link } from 'react-router-dom'

const Nav = () => {
  return (
    <nav>
        <Link to="/" className="d-flex justify-content-center">
            <img src="/images/brawlclub_logo.png" alt="logo" 
            className="" width="62px"/>
        </Link>
        <input id="menu-toggle" type="checkbox" />
        <label className='menu-button-container' htmlFor="menu-toggle">
            <div className='menu-button'></div>
        </label>
        <ul className="menu">
            <li>
                <Link to="/profile">Profile</Link>
            </li>
            <li>
                <Link to="/club">Club</Link>
            </li>
            <li>
                <Link to="leaderboard/players">Leaderboards</Link>
            </li>
        </ul>
        <ul>
            <li>
                <SearchBar />
            </li>
        </ul>
    </nav>
  )
}

export default Nav