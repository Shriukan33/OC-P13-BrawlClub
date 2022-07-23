import React from 'react'
import './Player.css'
import PlayerBcRating from './PlayerBcRating'
import PlayerProfile from "./PlayerProfile"
import PlayerStats from "./PlayerStats"
import {useState, useEffect, useRef} from 'react'
import { useParams } from 'react-router-dom'


const Player = () => {

  const [playerStats, setPlayerStats] = useState([])
  const [playerInstance, setPlayerInstance] = useState({})
  const { id } = useParams()
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
      fetchPlayerStats({id}.id).then((response) => {
          if (response.stats) {
            setPlayerStats(response.stats)
          } else {
            setPlayerStats([])
          }
          setPlayerInstance(response)
        })
      hasFetchedPlayer.current = true
      console.log(playerInstance)
    }
  }, [id])

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

      </div>

    </main>
  )
}

export default Player