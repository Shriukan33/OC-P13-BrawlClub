import React from 'react'
import './Leaderboard.css'
import LeaderboardLine from './LeaderboardLine'

const Leaderboard = ({title, topEntities, path, starting_index}) => {

  return (
    <>
    <div className="leadheader">
      <header className="mx-auto mt-2">{title}</header>
      </div>
      <div className="d-flex flex-column p-1 leaderboard-body mb-2">
        {topEntities.length ?
          topEntities.map((entity, index) => (
            <LeaderboardLine
              key={entity.player_tag ?? entity.club_tag}
              entity={entity}
              path={path}
              ranking={starting_index ? starting_index + index : 0 + index} />
          ))
          :
          <div className="d-flex justify-content-center">No player or club found</div>
        }
      </div>
    </>
  )
}

export default Leaderboard