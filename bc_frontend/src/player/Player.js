import React from 'react'
import './Player.css'
import PlayerBcRating from './PlayerBcRating'
import PlayerProfile from "./PlayerProfile"
import PlayerStats from "./PlayerStats"

const Player = () => {
  const playerStats = [
    {
      statName: "3v3 victories",
      statValue: 14222,
      statIcon: "3v3"
    },
    {
      statName: "Duo victories",
      statValue: 1227,
      statIcon: "duo"
    },
    {
      statName: "Solo victories",
      statValue: 1347,
      statIcon: "solo"
    },
    {
      statName: "Highest Trophies",
      statValue: 28250,
      statIcon: "trophy"
    },
    {
      statName: "Club war win rate",
      statValue: "94%",
      statIcon: "club_league_icon"
    },
    {
      statName: "Total tickets spent",
      statValue: 597,
      statIcon: "ticket"
    }
  ]

  return (
    <main className='col-10 col-lg-7 Player justify-content-center'>
      <div className="d-flex flex-row flex-wrap justify-content-center mx-auto">
        <div className="d-flex flex-column col-12 col-xl-4">
          <PlayerProfile />
        </div>
        <div id="Rating-and-stats" className="d-flex flex-column col-12 col-xl-8 ml-2">
          <PlayerBcRating bcRating={'94.58'} />
          <PlayerStats stats={playerStats} />
        </div>

      </div>

    </main>
  )
}

export default Player