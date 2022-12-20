import React from "react";
import { useState, useEffect, useRef } from "react";
import { Link } from "react-router-dom";
import ResultsTable from "./ResultsTable";
import "./Results.css";

const Results = () => {
  const [results, setResults] = useState([]);
  const resultsLoaded = useRef(false);

  useEffect(() => {
    let params = new URL(document.location).searchParams.toString();
    const API_URL = process.env.REACT_APP_API_ENDPOINT;
    const fetchResults = async (params) => {
      const response = await fetch(
        `${API_URL}/api/club-finder/results?${params}`
      );
      if (response.ok) {
        const json = await response.json();
        return json;
      }
    };
    if (!resultsLoaded.current) {
      fetchResults(params).then((response) => {
        setResults(response);
      });
      resultsLoaded.current = true;
    }
  }, []);

  return (
    <main className="col-11 col-lg-7 Player justify-content-center">
      <button className="back-btn d-flex me-auto mb-2">
        <Link to="/club-finder">
          <i className="fa-solid fa-arrow-left"></i>&nbsp;Back to filters
        </Link>
      </button>
      <section name="results">
        <ResultsTable results={results} />
      </section>
    </main>
  );
};

export default Results;
