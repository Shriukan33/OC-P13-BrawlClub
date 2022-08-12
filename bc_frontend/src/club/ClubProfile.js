import React from 'react'

const ClubProfile = ({ club }) => {
  return (
    <div className="PlayerProfile d-flex flex-column p-2 w-100 h-100">
        <div className='d-flex flex-row'>
            <div id="PlayerProfilePicture">
                <img src="/images/Player/Portrait_placeholder.png" alt="Player profile pic"/>
            </div>
            <div id="PlayerIdentity" className="d-flex flex-column mleft-2">
                <span>{club.club_name}</span>
                <span>{club.club_tag}</span>
            </div>
        </div>
        <p >{club.club_description}</p>
        <div id="PlayerProfileMetrics" className="d-flex flex-row my-auto justify-content-evenly">
            <div id="PlayerLevel" className="d-flex flex-column m-auto ">
                <span className="mright-2 m-auto">Type</span>
                <span>{club.club_type}</span>
            </div>
            <div id="PlayerTotalTrophies" className="d-flex flex-column m-auto flex-wrap">
                <span className="m-auto ">Required trophies</span>
                <div className="m-auto">
                    <img src="/images/Player/trophy.png" alt="Player trophies" />
                    <span className="m-auto">{club.required_trophies}</span>
                </div>
            </div>
        </div>
    </div>
  )
}

export default ClubProfile