import React from 'react'
import './PlayerStatLine.css'

const PlayerStatLine = ({statName, statValue, statIcon}) => {
  return (
    <div className='PlayerStatLine d-flex col-12 col-md-49 p-1 mb-1 justify-content-between'>
        
        <div className="d-flex align-items-center">
          <img className="stat-line-icon" src={`/images/Player/${statIcon}.png`} alt="stat icon" />
          <span className="stat-name-text">{statName}&nbsp;:&nbsp;</span>
        </div>
        
        <span className="my-auto">{statValue}</span>
    </div>
  )
}

export default PlayerStatLine