import React from 'react'
import './PlayerBcRating.css'

const PlayerBcRating = ({ bcRating }) => {
  var rank = ""
  var rating = parseFloat(bcRating)
  if (rating >= 0 && rating < 25) {
    rank = "bronze"
  } else if (rating >= 25 && rating < 45) {
    rank = "silver"
  }
  else if (rating >= 45 && rating < 60) {
    rank = "gold"
  }
  else if (rating >= 60 && rating < 75) {
    rank = "diamond"
  }
  else if (rating >= 75 && rating < 85) {
    rank = "mythic"
  }
  else if (rating >= 85 && rating < 95) {
    rank = "legendary"
  }
  else if (rating >= 95 && rating <= 100) {
    rank = "master"
  }
  return (
    <section id="BcRating" className={`d-flex flex-row flex-nowrap align-items-center mb-2 ${rank}`}>
        <img className="d-flex img-fluid" src={`/images/${rank}.png`} alt="club_league_icon" />
        <span className="d-flex">
          BrawlClub League Rating&nbsp;:&nbsp;{parseFloat(bcRating).toFixed(2)}
        </span>
    </section>
  )
}

export default PlayerBcRating