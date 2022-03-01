// import "./styles.css";
import React from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer
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
<BarChart width={730} height={500} data={data}>
  <CartesianGrid strokeDasharray="3 3" />
  <XAxis dataKey="name" label={{ value: 'Time', offset: "-5", position: 'insideBottom' }}/>
  <YAxis label={{ value: 'Average Acceleration', angle: -90, position: 'insideLeft' }}/>
  <Tooltip />
  <Bar dataKey="Acceleration" fill="#8884d8" />
</BarChart>
);
}
export default Chart;