// import "./styles.css";
import React from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer
} from "recharts";


function WoofLineChart({ data_name, timeseries, xLabel, yLabel, yFontSize = 24, yPosition = "insideLeft" }) {
  console.log(data_name);
  console.log(timeseries);
  return (

    <div className="container">
      <h3>{data_name}</h3>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={timeseries} margin={{ top: 20, right: 20, bottom: 40, left: 20 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <YAxis label={{ value: yLabel, angle: -90, position: yPosition, fontSize: yFontSize }} />
          <XAxis type="category" dataKey="Time" fontSize={15} label={{ value: xLabel, offset: -15, position: 'insideBottom' }} />
          <Tooltip />
          <Line type="monotone" dataKey="Value" stroke="#8884d8" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
export default WoofLineChart;