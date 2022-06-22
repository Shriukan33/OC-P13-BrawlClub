import React from 'react'
import "./PlayerProfile.css"

const PlayerProfile = () => {
  return (
    <div className="PlayerProfile d-flex flex-column p-2 col-10 col-lg-3 mx-auto">
        <div className='d-flex flex-row'>
            <div id="PlayerProfilePicture">
                <img src="/images/Portrait_placeholder.png" alt="Player profile pic"/>
            </div>
            <div id="PlayerIdentity" className="d-flex flex-column mleft-2">
                <span>Poulet</span>
                <span>Aquablue</span>
                <span>#ABCDE123</span>
            </div>
        </div>
        <div id="PlayerProfileMetrics" className="d-flex flex-row mt-2">
            <div id="PlayerLevel" className="d-flex mx-2 my-auto ">
                <span className="mright-2 my-auto">Level&nbsp;:</span>
                <div className="level-badge">
                    <img className="level-icon " src="/images/level.png" alt="Player level" />
                    <span>150</span>
                </div>
            </div>
            <div id="PlayerTotalTrophies" className="d-flex mx-2 my-auto flex-wrap">
                <span className="m-auto">Total of Trophies&nbsp;:</span>
                <div className="m-auto">
                    <img className="mleft-2" src="/images/trophy.png" alt="Player trophies" />
                    <span className="m-auto">28250</span>
                </div>
            </div>
        </div>
    </div>
  )
}

export default PlayerProfile