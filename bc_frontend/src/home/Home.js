import React from 'react'
import './Home.css'
import StaticSearchBar from "./StaticSearchBar"
import Leaderboard from './Leaderboard'
import { useState, useEffect, useRef } from 'react'

const Home = () => {

  
  const [topPlayers, setTopPlayers] = useState([])
  const [topClubs, setTopClubs] = useState([])
  const hasFetched = useRef(false)

  useEffect(() => {
    const API_URL = process.env.REACT_APP_API_ENDPOINT
    const fetchTopEntities = async (entity) => {
      const response = await fetch(`${API_URL}/top-${entity}`)
      if (response.ok) {
        const json = await response.json()
        return json
      }
    }

    if (!hasFetched.current) {
      fetchTopEntities("players").then(setTopPlayers)
      fetchTopEntities("clubs").then(setTopClubs)
      hasFetched.current = true
    }
  }, [])

  return (
    <main className='HomePage'>
        <img src="/images/brawlclub_logo.png" alt="Brawlclub logo" className="img-fluid d-flex col-10 col-md-5 col-lg-3 py-3"></img>
        <div className="my-5">
          <StaticSearchBar />
        </div>
        <section className="d-flex flex-wrap col-10 justify-content-center mx-auto">
          <Leaderboard title="Player Rating Leaderboard" topEntities={topPlayers} path="player"/>
          <Leaderboard title="Club Leaderboard" topEntities={topClubs} path="club" />
        </section>
    </main>
  )
}

export default Home
