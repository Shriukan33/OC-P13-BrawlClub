import React from 'react'
import PlayerStatLine from './PlayerStatLine'

const PlayerStats = ({stats}) => {
  return (
    <section id="PlayerStats" className='d-flex flex-row flex-wrap justify-content-evenly w-100' >
        {stats.length ? stats.map((stat, index) => {
            return <PlayerStatLine key={index} 
            statName={stat.statName}
            statValue={stat.statValue}
            statIcon={stat.statIcon} />
        }): <div>No stats available</div>}
    </section>
  )
}

export default PlayerStats