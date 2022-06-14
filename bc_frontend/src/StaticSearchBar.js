import React from 'react'
import styles from './StaticSearchBar.module.css'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faSearch } from '@fortawesome/free-solid-svg-icons'

const StaticSearchBar = () => {
  return (
    <form method='POST' action='#' onSubmit={(e) => e.preventDefault()}
    className="d-flex flex-row justify-content-center">
        <input type="text" className={styles["input-search"]+" d-flex col-12"} placeholder="Enter a player or a club tag"/>
        <button className={styles["btn-search"] + " px-3"}>
            <FontAwesomeIcon icon={faSearch} />
        </button>
    </form>
  )
}

export default StaticSearchBar