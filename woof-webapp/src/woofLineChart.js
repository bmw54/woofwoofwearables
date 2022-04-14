// import "./styles.css";
import React from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip
} from "recharts";


function WoofLineChart({ data_name }) {
  const timeSeries = [
    { time: 1, value: 2 },
    { time: 2.5, value: -2 },
    { time: 3.2, value: 1.22 },
    { time: 4.4, value: 0.1 },
    { time: 5.96, value: -0.8 },
    { time: 6.3, value: -4 },
    { time: 7, value: 4 }
  ];
  return (
    <LineChart width={500} height={400} data={timeSeries}
      margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="time" />
      <YAxis label={{ value: data_name, angle: -90, position: 'insideLeft' }} />
      <XAxis label={{ value: 'time', offset: -5, position: 'insideBottom' }} />
      <Tooltip />
      <Line type="monotone" dataKey="value" stroke="#8884d8" />
    </LineChart>
  );
}
export default WoofLineChart;