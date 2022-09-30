import React from 'react'
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Filler,
    Legend,
} from 'chart.js';
import { Line } from 'react-chartjs-2';
import "./PlayerAreaGraph.css"

const PlayerAreaGraph = ({history}) => {
    ChartJS.register(
        CategoryScale,
        LinearScale,
        PointElement,
        LineElement,
        Title,
        Tooltip,
        Filler,
        Legend
        );

    const options = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: false,
                position: 'top',
                color: 'black',
            },
            title: {
                display: true,
                text: 'Brawclub rating history',
                color: 'black',
            },
        },
        scales: {
            y: {
                beginAtZero: true,
                ticks : {
                    color: "black",
                },
            },
            x: {
                ticks : {
                    color: "black",
                }
            }
        },
    };
    const labels = history.map((item) => {
        let var_date = item.snapshot_date
        let date = new Date(var_date)
        let short_date = date.toLocaleDateString()
        return short_date
    })
    const _data = history.map((item) => {
        return item.brawlclub_rating
    })


    const data = {
        labels,
        datasets: [
            {
                fill: true,
                label: 'Brawlclub rating',
                data: _data,
                borderColor: 'rgba(240, 25, 25, 0.7)',
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                color: '#000'
            },
        ],
    };
    


    return (
        <Line options={options} data={data} />
    )
}

export default PlayerAreaGraph