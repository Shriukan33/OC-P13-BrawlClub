/* eslint-disable react/style-prop-object */
import React from "react";
import "./Footer.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faLinkedin } from "@fortawesome/free-brands-svg-icons";
import { faGithub } from "@fortawesome/free-brands-svg-icons";

const Footer = () => {
  return (
    <footer className="Footer">
      <div class="">
        This content is not affiliated with, endorsed, sponsored, or
        specifically approved by Supercell and Supercell is not responsible for
        it. For more information see
        <div className="Footlink">
          <a
            href="https://supercell.com/en/fan-content-policy/"
            target="_blank"
            rel="noreferrer"
          >
            Supercell's Fan Content Policy
          </a>
        </div>
        <span>Copyright © 2022 </span>
        <span>
          <a href="https://www.linkedin.com/in/benjamin-mourgues-33000/">
            <FontAwesomeIcon icon={faLinkedin} /> Mourgues Benjamin
          </a>
        </span>
        <span>
          <a href="https://github.com/Shriukan33/OC-P13-BrawlClub">
            <FontAwesomeIcon icon={faGithub} /> Github
          </a>
        </span>
      </div>
    </footer>
  );
};

export default Footer;
