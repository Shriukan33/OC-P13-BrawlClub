import React from 'react'
import "./SearchBar.css"
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faSearch } from '@fortawesome/free-solid-svg-icons'
import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

const SearchBar = () => {
  const [searchValue, setSearchValue] = useState('')
  const navigate = useNavigate()
  const handleSubmit = (e) => {
    e.preventDefault()
    // Need to check if this is a valid player or club
    // Check what sort of entity it is (Tag is either player or club)
    navigate(`/player/${searchValue}`)
    setSearchValue('')
  }
  const handleChange = (e) => {
    let new_value = e.target.value
    new_value = new_value.replaceAll('#', '')
    setSearchValue(new_value) 
  }

  return (
    <form className="search-box" onSubmit={handleSubmit}>
        <button type="button" className="btn-search">
            <FontAwesomeIcon icon={faSearch} />
        </button>
        <input type="text" className="input-search" placeholder="Enter a player or a club tag"
          onChange={handleChange}/>
    </form>
  )
}

export default SearchBar