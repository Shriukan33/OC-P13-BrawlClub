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
        <ul className="nav-elements">
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
        <ul className="searchBar">
            <li>
                <SearchBar />
            </li>
        </ul>
    </nav>
  )
}

export default Nav