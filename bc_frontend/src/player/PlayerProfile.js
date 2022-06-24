import React from 'react'
import "./PlayerProfile.css"

const PlayerProfile = () => {
  return (
    <div className="PlayerProfile d-flex flex-column p-2 w-100 h-100">
        <div className='d-flex flex-row'>
            <div id="PlayerProfilePicture">
                <img src="/images/Player/Portrait_placeholder.png" alt="Player profile pic"/>
            </div>
            <div id="PlayerIdentity" className="d-flex flex-column mleft-2">
                <span>Poulet</span>
                <span>Aquablue</span>
                <span>#ABCDE123</span>
            </div>
        </div>
        <div id="PlayerProfileMetrics" className="d-flex flex-row my-auto justify-content-evenly">
            <div id="PlayerLevel" className="d-flex flex-column m-auto ">
                <span className="mright-2 m-auto">Level</span>
                <div className="level-badge">
                    <img className="level-icon " src="/images/Player/level.png" alt="Player level" />
                    <span>150</span>
                </div>
            </div>
            <div id="PlayerTotalTrophies" className="d-flex flex-column m-auto flex-wrap">
                <span className="m-auto ">Trophies</span>
                <div className="m-auto">
                    <img src="/images/Player/trophy.png" alt="Player trophies" />
                    <span className="m-auto">28250</span>
                </div>
            </div>
        </div>
    </div>
  )
}

export default PlayerProfile