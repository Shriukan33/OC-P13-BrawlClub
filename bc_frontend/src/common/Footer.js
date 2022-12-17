/* eslint-disable react/style-prop-object */
import React from "react";
import "./Footer.css";

const Footer = () => {
  return (
    <footer className="text-center text-white footer copyrightsec">
      {/* Grid container*/}
      <div>
        {/* Section: Text*/}
        <section>
          <p
            style={{
              paddingTop: "10px",
              paddingBottom: "10px",
              marginBottom: "0px",
              textDecoration: "none",
            }}
          >
            This content is not affiliated with, endorsed, sponsored, or
            specifically approved by Supercell and Supercell is not responsible
            for it. For more information
            <br></br>
            <a
              className="btn btn-primary btn-floating m-1"
              style={{
                backgroundColor: "rgb(21 53 118)",
                borderBlockColor: "rgb(21 53 118)",
              }}
              href="https://supercell.com/en/fan-content-policy/"
              target="_blank"
              rel="noreferrer"
              role="button"
            >
              Supercell's Fan Content Policy
            </a>
          </p>
        </section>

        <section className="linksec" style={{}}>
          {/* Copyright*/}

          {/* <div className="text-center">
      <div style={{padding:"5px",textDecoration: "none"}}>© 2022 Copyright :  <a className="text-white" href="\"> BrawlClub™</a></div>
    </div>
    <div style={{paddingRight:"100px"}}>
    </div> */}

          {/* Section: Social media*/}
          <div>
            {/* unused Socials */}

            {/* Facebook*/}
            {/* <a className="btn btn-primary btn-floating m-1" style={{backgroundColor: "#3b5998"}} href="#!" role="button"><i className="fab fa-facebook-f"></i></a> */}

            {/* Twitter*/}
            {/* <a className="btn btn-primary btn-floating m-1" style={{backgroundColor: "#55acee"}} href="#!" role="button"><i className="fab fa-twitter"></i></a> */}

            {/* Google*/}
            {/* <a className="btn btn-primary btn-floating m-1" style={{backgroundColor: "#dd4b39"}} href="#!" role="button"><i className="fab fa-google"></i></a> */}

            {/* Instagram*/}
            {/* <a className="btn btn-primary btn-floating m-1" style={{backgroundColor: "#ac2bac"}} href="#!" role="button"><i className="fab fa-instagram"></i></a> */}

            {/* used Socials */}

            {/* Linkedin*/}
            <a
              className="btn btn-primary btn-floating m-1"
              style={{ backgroundColor: "#0082ca" }}
              href="https://www.linkedin.com/in/benjamin-mourgues-33000/"
              role="button"
            >
              <i className="fab fa-linkedin-in"></i>
            </a>
            {/* Github*/}
            <a
              className="btn btn-primary btn-floating m-1"
              style={{ backgroundColor: "#333333" }}
              href="https://github.com/Shriukan33/OC-P13-BrawlClub"
              role="button"
            >
              <i className="fab fa-github"></i>
            </a>
            {/* Section: Social media*/}
          </div>
        </section>
      </div>
      {/* Grid container*/}

      {/* Copyright*/}
    </footer>
  );
};

export default Footer;
