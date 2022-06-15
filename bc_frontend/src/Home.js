import React from 'react'
import './Home.css'
import StaticSearchBar from "./StaticSearchBar"
import Leaderboard from './Leaderboard'

const Home = () => {
  return (
    <main className='HomePage'>
        <img src="/images/brawlclub_logo.png" alt="Brawlclub logo" className="img-fluid d-flex col-10 col-md-5 col-lg-3 py-3"></img>
        <div className="my-5">
          <StaticSearchBar />
        </div>
        <section className="d-flex flex-wrap col-10 justify-content-around mx-auto">
          <Leaderboard title="Player Rating Leaderboard"/>
          <Leaderboard title="Club Leaderboard" />
        </section>
    </main>
  )
}

export default Home
