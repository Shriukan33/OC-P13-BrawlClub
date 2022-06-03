import React from 'react'
import "./Nav.css"
import { Link } from 'react-router-dom'

const Nav = () => {
  return (
    <nav>
        <ul>
            <li>
                <Link to="/">Home</Link>
            </li>
            <li>
                <Link to="/profile">Profile</Link>
            </li>
            <li>
                <Link to="/club">Club</Link>
            </li>
            <li>
                <Link to="leaderboard">Leaderboard</Link>
            </li>
            <li>
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