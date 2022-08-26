import React from 'react'
import Leaderboard from '../home/Leaderboard'
import { useState, useEffect, useRef } from 'react'
import { Link } from 'react-router-dom'
import { useParams } from 'react-router-dom'
import { useNavigate } from 'react-router-dom'
import './Leaderboard_app.css'

const Leaderboard_app = () => {
  const [leaderboard, setLeaderboard] = useState([])
  const [nextUrl, setNextUrl] = useState(null)
  const [prevUrl, setPrevUrl] = useState(null)
  const [page_size, setPageSize] = useState(50)
  const [page, setPage] = useState(1)
  const { entity } = useParams()
  const hasFetched = useRef(false)

  const entity_type = entity === "players" ? "player" : "club"

  useEffect(() => {
    const API_URL = process.env.REACT_APP_API_ENDPOINT
    setPage(1)
    const fetchTopEntities = async (entity) => {
      const response = await fetch(
        `${API_URL}/api/leaderboard/${entity}/?page_size=${page_size}&page=${page}`)
      if (response.ok) {
        const json = await response.json()
        return json
      }
    }

    if (!hasFetched.current) {
      setPage(1)
      fetchTopEntities(entity).then(json => {
        setLeaderboard(json.results)
        setNextUrl(json.next)
        setPrevUrl(json.previous)
      })
    }
    hasFetched.current = true

  }, [entity])


  const updatePageAndPageSize = (url) => {

    if (!url) {
      return
    }
    const urlParams = new URL(url)
    const new_page = urlParams.searchParams.get("page")
    const new_page_size = urlParams.searchParams.get("page_size")
    if (new_page) {
      setPage(parseInt(new_page) - 1)
    } else {
      setPage(1)
    }
    if (new_page_size) {
      setPageSize(new_page_size)
    }
  }

  const handleNext = async () => {
    if (nextUrl) {
      const response = await fetch(`${nextUrl}`)
      if (response.ok) {
        const json = await response.json()
        setLeaderboard(json.results)
        setNextUrl(json.next)
        setPrevUrl(json.previous)
        updatePageAndPageSize(json.next)
      }
    }
  }

  const handlePrev = async () => {
    if (prevUrl) {
      const response = await fetch(`${prevUrl}`)
      if (response.ok) {
        const json = await response.json()
        setLeaderboard(json.results)
        setNextUrl(json.next)
        setPrevUrl(json.previous)
        if (json.previous) {
          updatePageAndPageSize(json.next)
        } else {
          setPage(1)
        }
      }
    } else {
      setPage(1)
    }
  }

  const handleToggle = (e) => {
    setPage(1)
    setPageSize(50)
    hasFetched.current = false
    if (e.target.textContent === "Clubs") {
      document.getElementById("leaderboard-clubs-toggle").classList.add("active")
      document.getElementById("leaderboard-players-toggle").classList.remove("active")
    } else {
      document.getElementById("leaderboard-players-toggle").classList.add("active")
      document.getElementById("leaderboard-clubs-toggle").classList.remove("active")
    }
  }

  var starting_index = (page - 1) * page_size

  return (
    <main className='col-10 col-lg-7 leaderboard_app justify-content-center'>
      <header>
        <Link onClick={handleToggle} to={`/leaderboard/players/`}>
          <button id="leaderboard-players-toggle"
            className={"leaderboard-toggle players " + (entity_type == "player" ? "active" : "")}>
            Players
          </button>
        </Link>
        
        <Link onClick={handleToggle} to={`/leaderboard/clubs/`}>
          <button id="leaderboard-clubs-toggle"
          className={"leaderboard-toggle clubs " + (entity_type == "club" ? "active" : "")}>
            Clubs
          </button>
        </Link>
      </header>
      <div className="d-flex flex-column justify-content-center mx-auto">
        <div className='d-flex justify-content-between col-10 col-md-4 my-3 mx-auto'>
          <button className="btn leaderboard-btn" onClick={handlePrev}>
            Previous
          </button>
          <button className="btn leaderboard-btn" onClick={handleNext}>
            Next
          </button>
        </div>
        <div className="leaderboard-frame d-flex flex-column col-12 col-md-4 my-3 mx-auto px-3">
          <Leaderboard
            title="Leaderboard"
            topEntities={leaderboard}
            path={entity_type}
            starting_index={starting_index} />
        </div>
        <div className='d-flex justify-content-between col-10 col-md-4 my-3 mx-auto'>
          <button className="btn leaderboard-btn" onClick={handlePrev}>
            Previous
          </button>
          <button className="btn leaderboard-btn" onClick={handleNext}>
            Next
          </button>
        </div>
      </div>

    </main>
  )
}

export default Leaderboard_app