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

const PlayerAreaGraph = ({player}) => {
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
    const labels = ['January', 'February', 'March', 'April', 'May', 'June', 'July'];

    const data = {
        labels,
        datasets: [
            {
                fill: true,
                label: 'Brawlclub rating',
                data: [77, 66, 99, 55, 44, 66, 88],
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