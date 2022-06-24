import React from 'react'
import './Player.css'
import PlayerBcRating from './PlayerBcRating'
import PlayerProfile from "./PlayerProfile"

const Player = () => {
  return (
    <main className='col-10 col-lg-7 Player justify-content-center'>
      <div className="d-flex flex-row flex-wrap justify-content-center mx-auto">
        <PlayerProfile />
        <PlayerBcRating bcRating={'94.58'} />
      </div>
        
    </main>
  )
}

export default Player