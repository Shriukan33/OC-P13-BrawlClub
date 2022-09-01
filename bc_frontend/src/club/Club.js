import React from 'react'
import {useState, useEffect, useRef} from 'react'
import ClubProfile from './ClubProfile'
import PlayerBcRating from '../player/PlayerBcRating'
import PlayerStats from '../player/PlayerStats'
import PlayerRadarGraph from '../player/PlayerRadarGraph'
import Leaderboard from '../home/Leaderboard'
import { useParams } from 'react-router-dom'


export const Club = () => {

    const [club, setClub] = useState({})
    const [clubStats, setClubStats] = useState([])
    const [clubMembers, setClubMembers] = useState([])
    const hasFetchedClub = useRef(false)
    const { tag } = useParams()

    useEffect(() => {
        const API_URL = process.env.REACT_APP_API_ENDPOINT
        const fetchClub = async (club_id) => {
            const response = await fetch(`${API_URL}/api/club/${club_id}`)
            if (response.ok) {
                const json = await response.json()
                return json
            }
        }
        const fetchClubMembers = async (club_id) => {
          const response = await fetch(`${API_URL}/api/club-members/${club_id}`)
          if (response.ok) {
            const json = await response.json()
            return json
          }
        }

        if (!hasFetchedClub.current) {
            fetchClub(tag).then((response) => {
                let clubStats = {}
                clubStats.stats = [
                    {
                      statName:"Avg Win Rate",
                      statValue: Math.round((parseFloat(response.avg_win_rate)*100))+"%",
                      statIcon:"club_league_icon"
                    },
                    {
                      statName:"Avg Play Rate",
                      statValue: Math.round((parseFloat(response.avg_play_rate)*100))+"%",
                      statIcon:"ticket"
                    },
                    {
                      statName:"Avg Teamplay Rate",
                      statValue: Math.round((parseFloat(response.avg_teamplay_rate)*100))+"%",
                      statIcon:"club_mate"
                    },
                    {
                      statName:"# of Players",
                      statValue: response.nb_of_players,
                      statIcon:"friends"
                    }
                ]
                setClubStats(clubStats.stats)
                setClub(response)
                fetchClubMembers(tag).then((response) => {
                  setClubMembers(response)
                })
            })
            hasFetchedClub.current = true
        }
    }, [tag])

    let statsToDisplay = [
      'Avg Win Rate',
      'Avg Play Rate',
      'Avg Teamplay Rate'
    ]
    let statslabels = ['Win Rate', 'Participation', 'Teamplay']

  return (
    <main className='col-10 col-lg-7 Player justify-content-center'>
      <div className="d-flex flex-row flex-wrap justify-content-center mx-auto">
        <div className="d-flex flex-column col-12 col-xxl-6">
          <ClubProfile club={club} />
        </div>
        <div id="Rating-and-stats" className="d-flex flex-column col-12 col-xxl-6 ml-2">
          <PlayerBcRating bcRating={club.avg_bcr} />
          <PlayerStats stats={clubStats} />
        </div>
        
        <div id="Player-graph" className="d-flex flex-column col-12 ml-2">
          <div className="PlayerRadarGraph d-flex mb-1">
            <PlayerRadarGraph
              stats={clubStats}
              statsToDisplay={statsToDisplay}
              statslabels={statslabels}
            />
          </div>
        </div>
        <section className="d-flex flex-wrap col-12 justify-content-center mx-auto">
          <div className="leaderboard-frame d-flex flex-column col-12 col-md-6 my-3 mx-5 px-3">
            <Leaderboard title="Club's BCR ranking" topEntities={clubMembers} path="player" />
          </div>
        </section>
      </div>
    </main>
  )
}
export default Club