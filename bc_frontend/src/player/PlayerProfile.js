import React from 'react'
import { Link } from 'react-router-dom'
import "./PlayerProfile.css"

const PlayerProfile = ({player}) => {
  return (
    <div className="PlayerProfile d-flex flex-column p-2 w-100 h-100">
        <div className='d-flex flex-row'>
            <div id="PlayerProfilePicture">
                <img src="/images/Player/Portrait_placeholder.png" alt="Player profile pic"/>
            </div>
            <div id="PlayerIdentity" className="d-flex flex-column mleft-2">
                <span>{player.player_name}</span>
                <span>
                {
                    player.club ?
                    <Link to={`/club/${player.club.club_tag.replace("#", "")}`}>{player.club.club_name} &nbsp;<i className="fa-solid fa-share-from-square"></i> </Link>
                    :
                    "Not in a club."
                }
                </span>
                <span>{player.player_tag}</span>
            </div>
        </div>
        <div id="PlayerProfileMetrics" className="d-flex flex-row my-auto justify-content-evenly">
            <div id="PlayerLevel" className="d-flex flex-column m-auto ">
                <span className="mright-2 m-auto">Level</span>
                <div className="level-badge">
                    <img className="level-icon " src="/images/Player/level.png" alt="Player level" />
                    <span>{player.level}</span>
                </div>
            </div>
            <div id="PlayerTotalTrophies" className="d-flex flex-column m-auto flex-wrap">
                <span className="m-auto ">Trophies</span>
                <div className="m-auto">
                    <img src="/images/Player/trophy.png" alt="Player trophies" />
                    <span className="m-auto">{player.trophy_count}</span>
                </div>
            </div>
        </div>
    </div>
  )
}

export default PlayerProfile