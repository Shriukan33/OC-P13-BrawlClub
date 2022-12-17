import React from "react";
import ResultsTableLine from "./ResultsTableLine";
import "./ResultsTable.css";

const ResultsTable = ({ results }) => {
  return (
    <div className="table-responsive">
      <table className="table table-sm">
        <thead>
          <tr>
            <th scope="col" className="results-head">
              #
            </th>
            <th scope="col" className="results-head">
              Club Name
            </th>
            <th scope="col" className="results-head">
              Rating
            </th>
            <th scope="col" className="d-none d-sm-table-cell results-head">
              Members
            </th>
            <th scope="col" className="d-none d-md-table-cell results-head">
              Trophy Count
            </th>
          </tr>
        </thead>
        <tbody>
          {results.length ? (
            results.map((result, index) => (
              <ResultsTableLine key={index} ranking={index + 1} club={result} />
            ))
          ) : (
            <tr>
              <td colSpan="5" className="text-center">
                No club found
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
};

export default ResultsTable;
