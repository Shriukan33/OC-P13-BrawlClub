import React from 'react'
import './PlayerBcRating.css'

const PlayerBcRating = ({ bcRating }) => {
  return (
    <div id="BcRating" className='d-flex flex-row flex-nowrap align-items-center p-2'>
        <img className="d-flex img-fluid" src="/images/club_league_icon.png" alt="club_league_icon" />
        <span className="d-flex">BrawlClub League Rating&nbsp;:&nbsp;{bcRating}</span>
    </div>
  )
}

export default PlayerBcRating