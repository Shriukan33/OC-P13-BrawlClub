import React from 'react'
import { Link } from 'react-router-dom'
import './LeaderboardLine.css'

const LeaderboardLine = ({ entity, path }) => {
  return (
    <div className='d-flex mt-1 justify-content-between'>
        <div className='leaderboard-line-name'>
          <Link to={`/${path}/${entity.id}`}>{entity.name}</Link>
        </div>
        <div className='leaderboard-line-metric'>{entity.metric}</div>
    </div>
  )
}

export default LeaderboardLine