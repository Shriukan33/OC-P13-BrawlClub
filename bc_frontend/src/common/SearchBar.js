import React from 'react'
import "./SearchBar.css"
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faSearch } from '@fortawesome/free-solid-svg-icons'
import { useNavigate } from 'react-router-dom'

const SearchBar = () => {
  const API_URL = process.env.REACT_APP_API_ENDPOINT
  const navigate = useNavigate()

  const handleSearch = (user_input) => {
    fetch(`${API_URL}/api/search/${user_input}`)
      .then(response => response.json())
      .then(json => {
        if (json.club_tag) {
          navigate(`/club/${json.club_tag.replace("#", "")}`)
        } else if (json.player_tag) {
          navigate(`/player/${json.player_tag.replace("#", "")}`)
        }
      })
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    let user_input = document.getElementById("nav-search").value 
    user_input = user_input.replaceAll('#', '')
    handleSearch(user_input)
    document.getElementById("nav-search").value = ''
  }

  return (
    <form className="search-box" onSubmit={handleSubmit}>
        <button type="button" className="btn-search">
            <FontAwesomeIcon icon={faSearch} />
        </button>
        <input id="nav-search" type="text" className="input-search"
        placeholder="Enter a player or a club tag" />
    </form>
  )
}

export default SearchBar