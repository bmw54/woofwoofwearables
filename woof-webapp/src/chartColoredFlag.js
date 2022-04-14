// import "./styles.css";
import React from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ReferenceArea
} from "recharts";

const CustomReferenceArea1 = props => {
  console.log(props);
  console.log(props.width);
  console.log(props.height);
  return (
    <rect
      // stroke="red"
      fill={props.color}
      opacity={0.3}
      x={80}
      y={5}
      width={props.width}
      height={props.height}
    />
  );
};
const CustomReferenceArea2 = props => {
  console.log(props);
  console.log(props.width);
  console.log(props.height);
  return (
    <rect
      // stroke="red"
      fill={props.color}
      opacity={0.3}
      x={80}
      y={290}
      width={props.width}
      height={props.height}
    />
  );
};

function ChartColoredFlag({ data_name }) {
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
    <LineChart width={730} height={500} data={timeSeries}
      margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
      <ReferenceArea x1={timeSeries[0].time} x2={timeSeries[timeSeries.length - 1].time} y1={0} y2={3} shape={<CustomReferenceArea1 color={"#c6ffc4"} />} />
      <ReferenceArea x1={timeSeries[0].time} x2={timeSeries[timeSeries.length - 1].time} y1={-4} y2={-1} shape={<CustomReferenceArea2 color={"#fcd7b6"} bottomFill={true} />} />

      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="time" />
      <YAxis label={{ value: data_name, angle: -90, position: 'insideLeft' }} />
      <XAxis label={{ value: 'time', offset: -5, position: 'insideBottom' }} />
      <Tooltip />
      <Line type="monotone" dataKey="value" stroke="#8884d8" />
    </LineChart>
  );
}
export default ChartColoredFlag;