import React from 'react'

const LeaderboardLine = ({ entity }) => {
  return (
    <div className='d-flex justify-content-between'>
        <div className='leaderboard-line-name'>{entity.name}</div>
        <div className='leaderboard-line-metric'>{entity.metric}</div>
    </div>
  )
}

export default LeaderboardLine