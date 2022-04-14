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

const CustomBar = (props) => {
  let { biasToRight, fill } = props;
  //business logic here to update fill color explicitly


  fill = (biasToRight) ? "#c6ffc4" : "#fcd7b6";
  console.log(fill);
  //use explicit fill here, or use the additional css class and make a css selector to update fill there
  return <rect fill={fill} />
};

function WoofBarChart({ data_name }) {
  const [bias, setBias] = useState([]);
  // let bias;
  useEffect(() => {
    const timeSeries = [
      { time: 1, left: 54, right: 46 },
      { time: 2.5, left: 40, right: 60 },
      { time: 3.2, left: 54, right: 46 },
      { time: 4.4, left: 50, right: 50 },
      { time: 5.96, left: 46, right: 54 },
      { time: 6.3, left: 45, right: 55 },
      { time: 7, left: 70, right: 30 }
    ];

    timeSeries.forEach(obj => {
      const newObj = {};
      newObj.time = obj.time;
      newObj.biasToRight = obj.right - obj.left;
      console.log(newObj);
      const temp = [...bias, newObj];
      setBias(prevState => ([...prevState, newObj]));
      // console.log
    });
  }, []);

  // console.log(bias);

  return (
    <BarChart width={500} height={300} data={bias} margin={{ top: 5, right: 30, left: 20, bottom: 5 }} layout="vertical">
      <CartesianGrid strokeDasharray="3 3" />
      {/* <XAxis dataKey="time" />
      <YAxis /> */}
      <Tooltip />
      <XAxis type="number" />
      <YAxis dataKey="time" type="category" scale="band" />
      {/* <Legend /> */}
      {/* <Bar dataKey="biasToRight" fill="#8884d8" /> */}
      <Bar dataKey="biasToRight">
        {bias.map((entry, index) => (
          <Cell fill={entry.biasToRight > 0 ? "#b1f2b1" : "#fcd7b6"} />
        ))}
      </Bar>
      {/* <Bar shape={CustomBar} /> */}
      <ReferenceLine x={0} stroke="#000" />
      {/* <Bar dataKey="uv" fill="#82ca9d" /> */}
    </BarChart>
  );
}
export default WoofBarChart;