import React from 'react'
import { Link } from 'react-router-dom'
import './LeaderboardLine.css'

const LeaderboardLine = ({ entity, path, ranking }) => {
  entity.name = entity.player_name ?? entity.club_name
  entity.id = entity.player_tag ?? entity.club_tag
  entity.id = entity.id.replace("#", "")
  entity.metric = entity.brawlclub_rating ?? entity.avg_bcr
  entity.metric = entity.metric.toFixed(2)
  return (
    <div className='mt-1'>
      <div className='ff'>
      <div className='gg'>
        <div className='leaderboard-line-name'>
          <Link to={`/${path}/${entity.id}`}>{ranking+1}.&nbsp;{entity.name}</Link>
        </div>
        <div className='leaderboard-line-metric'>{entity.metric}</div>
        </div>
        <div className="hiddeninfo">
          <p>Additional info here</p>
        </div>
        </div>
    </div>
  )
}

export default LeaderboardLine