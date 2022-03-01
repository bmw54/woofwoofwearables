// import "./styles.css";
import React from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
} from "recharts";

function Chart({}){

const data = [
  {
    name: "11:00",
    Acceleration: 3.21
  },
  {
    name: "11:30",
    Acceleration: 3.45
  },
  {
    name: "12:00",
    Acceleration: 9.55
  },
  {
    name: "12:30",
    Acceleration: 1.12
  },
  {
    name: "13:00",
    Acceleration: 0.20
  },
  {
    name: "13:30",
    Acceleration: 2.23
  },
  {
    name: "14:00",
    Acceleration: 3.34
  }
];
return (
<LineChart width={730} height={500} data={data}
  margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
  <CartesianGrid strokeDasharray="3 3" />
  <XAxis dataKey="name" />
  <YAxis label={{ value: 'Average Acceleration', angle: -90, position: 'insideLeft' }}/>
  <XAxis label={{ value: 'Time', offset: -5, position: 'insideBottom' }}/>
  <Tooltip/>
  <Line type="monotone" dataKey="Acceleration" stroke="#8884d8" />
</LineChart>
);
}
export default Chart;