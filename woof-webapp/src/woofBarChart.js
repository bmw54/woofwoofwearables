// import "./styles.css";
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
  Cell
} from "recharts";

function WoofBarChart({ data_name, timeseries }) {
  console.log(timeseries)
  return (
    <div className="container">
      <h3>{data_name}</h3>
      <BarChart width={350} height={300} data={timeseries} margin={{ top: 20, right: 20, bottom: 20, left: 10 }} layout="vertical">
        <CartesianGrid strokeDasharray="3 3" />
        <Tooltip />
        <XAxis type="number" label={{ value: 'Angle', offset: -10, position: 'insideBottom' }} />
        <YAxis dataKey="Time" type="category" scale="band" label={{ value: 'Time', angle: -90, position: 'insideLeft' }} />
        <Bar dataKey="Value">
          {timeseries.map((item) => (
            <Cell fill={item.Value > 0 ? "#b1f2b1" : "#fcd7b6"} />
          ))}
        </Bar>
        <ReferenceLine x={0} stroke="#000" />
      </BarChart>
    </div>
  );
}
export default WoofBarChart;