import React from 'react'
import {
    Chart as ChartJS,
    RadialLinearScale,
    PointElement,
    LineElement,
    Filler,
    Tooltip,
    Legend,
  } from 'chart.js';
import { Radar } from 'react-chartjs-2';
import "./PlayerRadarGraph.css"

const PlayerRadarGraph = ({stats, statsToDisplay, statslabels}) => {

    ChartJS.register(
        RadialLinearScale,
        PointElement,
        LineElement,
        Filler,
        Tooltip,
        Legend
      );

    const values = stats.map(
        stat => {
            return {statName: stat.statName, statValue: parseFloat(stat.statValue).toFixed(2)}
        }).filter((stat) => {
            return statsToDisplay.includes(stat.statName)
        }).map(stat => {
            return stat.statValue
        });

    const options = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: false,
                position: 'bottom',
                labels: {
                    color: 'white',
                    font: {
                        family: 'Poppins',
                        weight: 'bold',
                    } 
                }
            },
            title: {
                display: false,
                text: 'In %',
                color: 'white',
            },
        },
        scales: {
            r: {
                pointLabels: {
                    color: "white",
                    font: {
                        family: "Poppins",
                        weight: "bold",
                        size: 12,
                    }
                },
                ticks: {
                    backdropColor: 'rgba(255, 255, 255, 0)',
                    autoSkip: false,
                },
                beginAtZero: true,
                max: 100,
                min: 0,
            }
        }
    }

    const data = {
        labels: statslabels,
        datasets: [
        {
            label: 'In %',
            data: values,
            backgroundColor: 'rgba(0, 0, 0, 0)',
            borderColor: 'rgba(240, 25, 25, 0.7)',
            borderWidth: 4,
        },
        ],
    }; 

    return (
            <Radar data={data} options={options} />
    )
}

export default PlayerRadarGraph
