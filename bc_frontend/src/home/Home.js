import React from 'react'
import './Home.css'
import StaticSearchBar from "./StaticSearchBar"
import Leaderboard from './Leaderboard'
import { useState, useEffect, useRef } from 'react'


const Home = () => {

  
  const [topPlayers, setTopPlayers] = useState(
    localStorage.getItem("topPlayers") ?
      JSON.parse(localStorage.getItem("topPlayers")) : [])
  const [topClubs, setTopClubs] = useState(
    localStorage.getItem("topClubs") ?
      JSON.parse(localStorage.getItem("topClubs")) : [])
  const hasFetched = useRef(false)

  useEffect(() => {
    const API_URL = process.env.REACT_APP_API_ENDPOINT
    const fetchTopEntities = async (entity) => {
      const response = await fetch(`${API_URL}/api/leaderboard/${entity}/?page_size=10&page=1`)
      if (response.ok) {
        const json = await response.json()
        return json
      }
    }

    if (!hasFetched.current) {
      fetchTopEntities("players").then((response) => {
        setTopPlayers(response.results)
        localStorage.setItem("topPlayers", JSON.stringify(response.results))
      })
      fetchTopEntities("clubs").then((response) => {
        setTopClubs(response.results)
        localStorage.setItem("topClubs", JSON.stringify(response.results))
      })
      hasFetched.current = true
    }
  }, [])

  return (
    <main className='HomePage'>
    
    
    
    {/* Background image */}
<div className="bg-image" >
  <div className="mask">
    <div className="d-flex justify-content-center align-items-center h-100" style={{flexDirection: 'column'}}>
    <img src="/images/brawlclub_logo.png" alt="Brawlclub logo" className="img-fluid d-flex col-10 col-md-5 col-lg-3 py-3"></img>

    {/* searchbar  */}    

    <div className="my-5">
          <StaticSearchBar />
        </div>
    </div>
  </div>
</div>
{/* Background image */}
   

                {/* new proposed about-site section */}
                
                <section className="abtsec">
                <div className="abthead wave">
                  <h1>Curious about Your Rank?</h1>
                  <h3>Check it Out by Searching our database </h3>
                </div>
                
                {/* extra info section   */}
                <div className='py-5 px-5 mt-3 abtinfo'>
                <h4>Claire is a chicken Queen</h4>
                <p>Ben makes better cookies than claire</p>
               <p>The about and how to use goes here</p>
                </div>

                <section className="d-flex flex-wrap col-10 justify-content-center mx-auto plo">
          <div className="leaderboard-frame d-flex flex-column col-12 col-md-4 my-3 mx-5 px-3">
            <Leaderboard
              title="Player Rating Leaderboard"
              topEntities={topPlayers}
              path="player"/>
          </div>
          <div className="leaderboard-frame d-flex flex-column col-12 col-md-4 my-3 mx-5 px-3">
            <Leaderboard
              title="Club Leaderboard"
              topEntities={topClubs}
              path="club" />
          </div>
        </section>


        <section className="playlist">

        <div id="carouselExampleIndicators" class="carousel slide" data-ride="carousel">
  <ol class="carousel-indicators">
    <li data-target="#carouselExampleIndicators" data-slide-to="0" class="active"></li>
    <li data-target="#carouselExampleIndicators" data-slide-to="1"></li>
    <li data-target="#carouselExampleIndicators" data-slide-to="2"></li>
  </ol>
  <div class="carousel-inner">
    <div class="carousel-item active">
    <iframe width="560" height="315" src="https://www.youtube.com/embed/G_wxQe2Litw" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
      {/* <img class="d-block w-100" src="https://www.youtube.com/watch?v=G_wxQe2Litw" alt="First slide"></img> */}
    </div>
    <div class="carousel-item">
      <img class="d-block w-100" src="..." alt="Second slide"></img>
    </div>
    <div class="carousel-item">
      <img class="d-block w-100" src="..." alt="Third slide"></img>
    </div>
  </div>
  <a class="carousel-control-prev" href="#carouselExampleIndicators" role="button" data-slide="prev">
    <span class="carousel-control-prev-icon" aria-hidden="true"></span>
    <span class="sr-only">Previous</span>
  </a>
  <a class="carousel-control-next" href="#carouselExampleIndicators" role="button" data-slide="next">
    <span class="carousel-control-next-icon" aria-hidden="true"></span>
    <span class="sr-only">Next</span>
  </a>
</div>
        
        </section>
                </section>
    </main>
  )
}

export default Home
