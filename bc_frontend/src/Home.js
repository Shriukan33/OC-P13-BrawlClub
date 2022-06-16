import React from 'react'
import './Home.css'
import StaticSearchBar from "./StaticSearchBar"
import Leaderboard from './Leaderboard'
import { useState } from 'react'

const Home = () => {

  const [topPlayers, setTopPlayers] = useState([
    {
      id: 1,
      name: 'Player 1',
      metric: '99.5',
    },
    {
      id: 2,
      name: 'Player 2',
      metric: '94.57',
    },
    {
      id: 3,
      name: 'Player 3',
      metric: '92.5',
    },
    {
      id: 4,
      name: 'Player 4',
      metric: '91.5',
    },
    {
      id: 5,
      name: 'Player 5',
      metric: '90.5',
    },
    {
      id: 6,
      name: 'Player 6',
      metric: '89.5',
    },
    {
      id: 7,
      name: 'Player 7',
      metric: '88.5',
    },
    {
      id: 8,
      name: 'Player 8',
      metric: '87.5',
    },
    {
      id: 9,
      name: 'Player 9',
      metric: '86.5',
    },
    {
      id: 10,
      name: 'Player 10',
      metric: '85.5',
    }
  ])
  const [topClubs, setTopClubs] = useState([])

  // const fetchTopPlayers = async () => {
  //   const response = await fetch('/api/top_players')
  //   const json = await response.json()
  //   setTopPlayers(json)
  // }

  return (
    <main className='HomePage'>
        <img src="/images/brawlclub_logo.png" alt="Brawlclub logo" className="img-fluid d-flex col-10 col-md-5 col-lg-3 py-3"></img>
        <div className="my-5">
          <StaticSearchBar />
        </div>
        <section className="d-flex flex-wrap col-10 justify-content-around mx-auto">
          <Leaderboard title="Player Rating Leaderboard" topEntities={topPlayers}/>
          <Leaderboard title="Club Leaderboard" topEntities={topClubs} />
        </section>
    </main>
  )
}

export default Home
