import React, { useEffect, useState } from "react";
import {
    BarChart,
    Bar,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    Legend,
    ReferenceLine,
    Cell,
    ResponsiveContainer
} from "recharts";

const data = [
    {
        Time: 5,
        happy: 30,
        neutral: 25,
        sad: 5
    },
    {
        Time: 1,
        happy: 5,
        neutral: 54,
        sad: 1
    },
    {
        Time: 2,
        happy: 10,
        neutral: 40,
        sad: 10
    },
    {
        Time: 3,
        happy: 8,
        neutral: 46,
        sad: 6
    },
    {
        Time: 4,
        happy: 2,
        neutral: 46,
        sad: 2
    }

]

export default function WoofMultiBarChart() {
    return (
        <div className="container">
            <h3>Moods</h3>
            <ResponsiveContainer width="100%" height={300}>
                <BarChart width={350} height={300} data={data} margin={{ top: 5, right: 20, bottom: 20, left: 10 }}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <Tooltip />
                    <XAxis dataKey="Time" type="number" label={{ value: 'Hour', offset: -15, position: 'insideBottom' }} />
                    <YAxis label={{ value: 'Minutes in mood', angle: -90, offset: 10, position: 'insideBottomLeft' }} />
                    <Bar dataKey="happy" fill="#b1f2b1" />
                    <Bar dataKey="neutral" fill="#E5E5E5" />
                    <Bar dataKey="sad" fill="#fcd7b6" />
                    <Legend verticalAlign="top" />
                </BarChart>
            </ResponsiveContainer>
        </div>
    )
}