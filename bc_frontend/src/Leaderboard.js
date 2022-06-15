import React from 'react'
import './Leaderboard.css'

const Leaderboard = ({title}) => {

  return (
    <div className="leaderboard-frame d-flex col-10 col-md-4 my-1">
      <header className="mx-auto">{title}</header>

    </div>
  )
}

export default Leaderboard