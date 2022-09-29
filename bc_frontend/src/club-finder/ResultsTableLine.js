import React from 'react'
import { useNavigate } from 'react-router-dom'
import './ResultsTableLine.css'

const ResultsTableLine = ({club, ranking}) => {

    const navigate = useNavigate()
    const handleClick = (e) => {
        let cleaned_club_tag = club.club_tag.replace("#", "")
        navigate(`/club/${cleaned_club_tag}`)
    }

    return (
        <tr className={ranking %2 ? "results-line even" : "results-line odd"}
        onClick={handleClick}>
            <th scope="row">{ranking}</th>
            <td>{club.club_name}</td>
            <td>{club.avg_bcr}</td>
            <td className='d-none d-sm-table-cell'>{club.nb_of_players}/30</td>
            <td className='d-none d-md-table-cell'>
                {String(club.trophies).toLocaleString()}
            </td>
        </tr>
    )
}

export default ResultsTableLine