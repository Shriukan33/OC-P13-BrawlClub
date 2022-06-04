import React from 'react'
import './Footer.css'
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faLinkedin } from "@fortawesome/free-brands-svg-icons";
import { faGithub } from "@fortawesome/free-brands-svg-icons";


const Footer = () => {
  return (
    <footer className='Footer'>
        <span>Made by <a href='https://www.linkedin.com/in/benjamin-mourgues-33000/'><FontAwesomeIcon icon={faLinkedin} /> Mourgues Benjamin</a></span>
        <span><a href="https://github.com/Shriukan33/OC-P13-BrawlClub"><FontAwesomeIcon icon={faGithub} /> Github</a></span>
    </footer>
  )
}

export default Footer