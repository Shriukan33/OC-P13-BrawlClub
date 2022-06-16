import React from 'react'
import './Leaderboard.css'
import LeaderboardLine from './LeaderboardLine'

const Leaderboard = ({title, topEntities}) => {

  return (
    <div className="leaderboard-frame d-flex flex-column col-10 col-md-4 my-1">
      <header className="mx-auto">{title}</header>
      <div className="d-flex flex-column p-1 leaderboard-body">
        {topEntities.length ?
          topEntities.map(entity => (
            <LeaderboardLine key={entity.id} entity={entity} />
          ))
          :
          <div className="d-flex justify-content-center">No player or club found</div>
        }
      </div>
    </div>
  )
}

export default Leaderboard