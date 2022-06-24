import React from 'react'
import PlayerStatLine from './PlayerStatLine'

const PlayerStats = ({stats}) => {
  return (
    <section id="PlayerStats" className='d-flex flex-row flex-wrap justify-content-evenly' >
        {stats.map((stat, index) => {
            return <PlayerStatLine key={index} 
            statName={stat.statName}
            statValue={stat.statValue}
            statIcon={stat.statIcon} />
        })}
    </section>
  )
}

export default PlayerStats