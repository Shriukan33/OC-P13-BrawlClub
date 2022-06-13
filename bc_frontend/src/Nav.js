import React from 'react'
import "./Nav.css"
import { Link } from 'react-router-dom'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faSearch } from '@fortawesome/free-solid-svg-icons'

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
                <div className="searchIcon container">
                    <FontAwesomeIcon icon={faSearch}/>
                </div>
                <form className="searchForm" onSubmit={(e) => e.preventDefault()}>
                    <label htmlFor="search">Search</label>
                    <input 
                        id="search"
                        type="text" 
                        placholder="Enter a player or a club tag"
                    />
                </form>
            </li>
        </ul>
    </nav>
  )
}

export default Nav