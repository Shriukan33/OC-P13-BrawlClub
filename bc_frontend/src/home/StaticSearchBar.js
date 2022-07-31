import React from 'react'
import styles from './StaticSearchBar.module.css'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faSearch } from '@fortawesome/free-solid-svg-icons'
import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

const StaticSearchBar = () => {
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
    console.log(new_value)
    setSearchValue(new_value) 
  }
  return (
    <form onSubmit={handleSubmit}
    className="d-flex flex-row justify-content-center">
        <input type="text" className={styles["input-search"]+" d-flex"}
        placeholder="Enter a player or a club tag"
        onChange={handleChange}/>
        <button className={styles["btn-search"] + " px-3"}>
            <FontAwesomeIcon icon={faSearch} />
        </button>
    </form>
  )
}

export default StaticSearchBar