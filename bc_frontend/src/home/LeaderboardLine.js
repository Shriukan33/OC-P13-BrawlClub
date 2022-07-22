import React from 'react'
import { Link } from 'react-router-dom'
import './LeaderboardLine.css'

const LeaderboardLine = ({ entity, path }) => {
  entity.name = entity.player_name ?? entity.club_name
  entity.id = entity.player_tag ?? entity.club_tag
  entity.id = entity.id.replace("#", "")
  entity.metric = entity.brawlclub_rating ?? entity.avg_bcr
  entity.metric = entity.metric.toFixed(2)
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