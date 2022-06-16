import React from 'react'
import styles from "./SearchBar.css"
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faSearch } from '@fortawesome/free-solid-svg-icons'

const SearchBar = () => {
  return (
    <div className="search-box">
        <button className="btn-search">
            <FontAwesomeIcon icon={faSearch} />
        </button>
        <input type="text" className="input-search" placeholder="Enter a player or a club tag"/>
    </div>
  )
}

export default SearchBar