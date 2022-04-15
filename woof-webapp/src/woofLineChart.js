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


function WoofLineChart({ data_name, timeseries }) {

  return (
    <LineChart width={500} height={400} data={timeseries}
      margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="Time" />
      <YAxis label={{ value: data_name, angle: -90, position: 'insideLeft' }} />
      <XAxis label={{ value: 'Time', offset: -5, position: 'insideBottom' }} />
      <Tooltip />
      <Line type="monotone" dataKey="value" stroke="#8884d8" />
    </LineChart>
  );
}
export default WoofLineChart;