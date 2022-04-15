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
      <YAxis label={{ value: data_name, angle: -90, position: 'insideLeft' }} />
      <XAxis type = "number" dataKey = "Time" label={{ value: 'Seconds', offset: -10, position: 'insideBottom' }}/>
      <Tooltip />
      <Line type="monotone" dataKey="Value" stroke="#8884d8" />
    </LineChart>
  );
}
export default WoofLineChart;