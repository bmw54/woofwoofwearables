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

    <div className="container">
      <h3>{data_name}</h3>
      <LineChart width={350} height={300} data={timeseries} margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
        <CartesianGrid strokeDasharray="3 3" />
        <YAxis label={{ value: "Degrees", angle: -90, position: 'insideLeft' }} />
        <XAxis type = "number" dataKey = "Time" label={{ value: 'Seconds', offset: -10, position: 'insideBottom' }}/>
        <Tooltip />
        <Line type="monotone" dataKey="Value" stroke="#8884d8" />
      </LineChart>
    </div>
  );
}
export default WoofLineChart;