import React from 'react'
import "./SearchBar.css"
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faSearch } from '@fortawesome/free-solid-svg-icons'

const SearchBar = () => {
  return (
    <div class="search-box">
        <button class="btn-search">
            <FontAwesomeIcon icon={faSearch} />
        </button>
        <input type="text" class="input-search" placeholder="Enter a player or a club tag"/>
    </div>
  )
}

export default SearchBar