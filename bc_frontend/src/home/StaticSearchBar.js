import React from "react";
import "./StaticSearchBar.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faSearch } from "@fortawesome/free-solid-svg-icons";
import { useState } from "react";
import { useNavigate } from "react-router-dom";

const StaticSearchBar = () => {
  const API_URL = process.env.REACT_APP_API_ENDPOINT;
  const [searchResultNotFound, setSearchResultNotFound] = useState(false);
  const navigate = useNavigate();

  const handleSearch = (user_input) => {
    fetch(`${API_URL}/api/search/${user_input}`)
      .then((response) => response.json())
      .then((json) => {
        if (json.club_tag) {
          navigate(`/club/${json.club_tag.replace("#", "")}`);
        } else if (json.player_tag) {
          navigate(`/player/${json.player_tag.replace("#", "")}`);
        } else {
          setSearchResultNotFound(true);
        }
      });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    let user_input = document.getElementById("staticsearchbar-input").value;
    user_input = user_input.replaceAll("#", "");
    handleSearch(user_input);
    document.getElementById("staticsearchbar-input").value = "";
  };

  return (
    <>
      <form
        onSubmit={handleSubmit}
        className="d-flex flex-row justify-content-center srchbar"
      >
        <input
          id="staticsearchbar-input"
          type="text"
          className="input-search d-flex"
          maxLength="9"
          placeholder="#XXXXXXXXX"
        />
        <button className="btn-search px-3" type="submit">
          <FontAwesomeIcon icon={faSearch} />
        </button>
      </form>

      {searchResultNotFound && (
        <span className="error-text">No results for this tag</span>
      )}
    </>
  );
};

export default StaticSearchBar;
