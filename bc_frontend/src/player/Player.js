import React from 'react'
import './Player.css'
import PlayerBcRating from './PlayerBcRating'
import PlayerProfile from "./PlayerProfile"
import PlayerStats from "./PlayerStats"
import {useState, useEffect} from 'react'
import { useParams } from 'react-router-dom'


const Player = () => {
  
  const [playerStats, setPlayerStats] = useState([])
  const [player_bc_rating, setPlayerBcRating] = useState('')
  const { id } = useParams()

  useEffect(() => {
    const API_URL = process.env.REACT_APP_API_ENDPOINT
    const fetchPlayerStats = async (player_id) => {
      const response = await fetch(`${API_URL}/player/${player_id}`)
      if (response.ok) {
        const json = await response.json()
        return json
      }
    }
    
    fetchPlayerStats({id}.id).then((response) => {
        if (response.stats) {
          setPlayerStats(response.stats)
        } else {
          setPlayerStats([])
        }
        if (response.Bc_rating) {
          setPlayerBcRating(response.Bc_rating)
        } else {
          setPlayerBcRating('Unknown')
        }
      })
  }, [id])

  return (
    <main className='col-10 col-lg-7 Player justify-content-center'>
      <div className="d-flex flex-row flex-wrap justify-content-center mx-auto">
        <div className="d-flex flex-column col-12 col-xl-4">
          <PlayerProfile />
        </div>
        <div id="Rating-and-stats" className="d-flex flex-column col-12 col-xl-8 ml-2">
          <PlayerBcRating bcRating={player_bc_rating} />
          <PlayerStats stats={playerStats} />
        </div>

      </div>

    </main>
  )
}

export default Player