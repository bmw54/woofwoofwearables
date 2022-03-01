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
    Acceleration: 4000
  },
  {
    name: "11:30",
    Acceleration: 3000
  },
  {
    name: "12:00",
    Acceleration: 2000
  },
  {
    name: "12:30",
    Acceleration: 2780
  },
  {
    name: "13:00",
    Acceleration: 1890
  },
  {
    name: "13:30",
    Acceleration: 2390
  },
  {
    name: "14:00",
    Acceleration: 3490
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