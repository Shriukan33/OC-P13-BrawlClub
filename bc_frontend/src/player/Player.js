import React from 'react'
import './Player.css'
import PlayerBcRating from './PlayerBcRating'
import PlayerProfile from "./PlayerProfile"
import PlayerStats from "./PlayerStats"
import PlayerAreaGraph from './PlayerAreaGraph'
import PlayerRadarGraph from './PlayerRadarGraph'
import {useState, useEffect, useRef} from 'react'
import { useParams } from 'react-router-dom'


const Player = () => {

  const [playerStats, setPlayerStats] = useState([])
  const [playerInstance, setPlayerInstance] = useState({})
  const { tag } = useParams()
  const hasFetchedPlayer = useRef(false)

  useEffect(() => {
    const API_URL = process.env.REACT_APP_API_ENDPOINT
    const fetchPlayerStats = async (player_id) => {
      const response = await fetch(`${API_URL}/api/player/${player_id}`)
      if (response.ok) {
        const json = await response.json()
        return json
      }
    }
    if (!hasFetchedPlayer.current) {
      fetchPlayerStats({tag}.tag).then((response) => {
          let playerStats = {}
          playerStats.stats = [
            {statName: "3v3 wins", statValue: response.total_3v3_wins, statIcon: "3v3"},
            {statName: "Club league win rate", statValue: parseFloat(response.club_league_winrate).toFixed(2)*100+"%", statIcon: "club_league_icon"},
            {statName: "Club league play rate", statValue: parseFloat(response.club_league_playrate).toFixed(2)*100+"%", statIcon: "ticket"},
            {statName: "Club league teamplay rate", statValue: parseFloat(response.club_league_teamplay_rate).toFixed(2)*100+"%", statIcon: "club_mate"},
          ]
          setPlayerStats(playerStats.stats)
          setPlayerInstance(response)
        })
      hasFetchedPlayer.current = true
      console.log(playerInstance)
    }
  }, [tag])

  return (
    <main className='col-10 col-lg-7 Player justify-content-center'>
      <div className="d-flex flex-row flex-wrap justify-content-center mx-auto">
        <div className="d-flex flex-column col-12 col-xl-4">
          <PlayerProfile player={playerInstance}/>
        </div>
        <div id="Rating-and-stats" className="d-flex flex-column col-12 col-xl-8 ml-2">
          <PlayerBcRating
          bcRating={playerInstance ? playerInstance.brawlclub_rating : "Unknown"} />
          <PlayerStats stats={playerStats} />
        </div>
        
        <div id="Player-graph" className="d-flex flex-column col-12 ml-2">
          <div className="PlayerRadarGraph d-flex">
            <PlayerRadarGraph stats={playerStats} />
          </div>
          <div className="PlayerAreaGraph d-flex">
            <PlayerAreaGraph stats={playerStats} />
          </div>
        </div>

      </div>

    </main>
  )
}

export default Player