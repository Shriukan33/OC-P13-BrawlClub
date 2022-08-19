import React from 'react'
import './Home.css'
import StaticSearchBar from "./StaticSearchBar"
import Leaderboard from './Leaderboard'
import { useState, useEffect, useRef } from 'react'

const Home = () => {

  
  const [topPlayers, setTopPlayers] = useState(
    localStorage.getItem("topPlayers") ?
      JSON.parse(localStorage.getItem("topPlayers")) : [])
  const [topClubs, setTopClubs] = useState(
    localStorage.getItem("topClubs") ?
      JSON.parse(localStorage.getItem("topClubs")) : [])
  const hasFetched = useRef(false)

  useEffect(() => {
    const API_URL = process.env.REACT_APP_API_ENDPOINT
    const fetchTopEntities = async (entity) => {
      const response = await fetch(`${API_URL}/api/leaderboard/${entity}/?page_size=10&page=1`)
      if (response.ok) {
        const json = await response.json()
        return json
      }
    }

    if (!hasFetched.current) {
      fetchTopEntities("players").then((response) => {
        setTopPlayers(response.results)
        localStorage.setItem("topPlayers", JSON.stringify(response.results))
      })
      fetchTopEntities("clubs").then((response) => {
        setTopClubs(response.results)
        localStorage.setItem("topClubs", JSON.stringify(response.results))
      })
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
          <div className="leaderboard-frame d-flex flex-column col-10 col-md-4 my-3 mx-5 px-3">
            <Leaderboard
              title="Player Rating Leaderboard"
              topEntities={topPlayers}
              path="player"/>
          </div>
          <div className="leaderboard-frame d-flex flex-column col-10 col-md-4 my-3 mx-5 px-3">
            <Leaderboard
              title="Club Leaderboard"
              topEntities={topClubs}
              path="club" />
          </div>
        </section>
    </main>
  )
}

export default Home
