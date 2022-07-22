import React from 'react'
import './Leaderboard.css'
import LeaderboardLine from './LeaderboardLine'

const Leaderboard = ({title, topEntities, path}) => {

  
  return (
    <div className="leaderboard-frame d-flex flex-column col-10 col-md-4 my-3 mx-5 px-3">
      <header className="mx-auto mt-2">{title}</header>
      <div className="d-flex flex-column p-1 leaderboard-body mb-2">
        {topEntities.length ?
          topEntities.map(entity => (
            <LeaderboardLine key={entity.player_tag ?? entity.club_tag} entity={entity} path={path} />
          ))
          :
          <div className="d-flex justify-content-center">No player or club found</div>
        }
      </div>
    </div>
  )
}

export default Leaderboard