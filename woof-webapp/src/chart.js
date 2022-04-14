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

function Chart({timeSeries, data_name}){

  // if(timeSeries.length > 20){
  //   timeSeries = timeSeries.slice(-20);
  // }
  let newTS = timeSeries;
  newTS = timeSeries.map((element) => { 
    
    console.log(element);
    let temp = new Date(element.Time);
    console.log(temp.toLocaleTimeString('en-GB'));
    const newElement = {};
    newElement.Time = temp.toLocaleTimeString('en-GB');
    newElement.Value = element.Value;
    
    // temp =  temp.toLocaleTimeString('en-GB');
    // element.Time = temp.toLocaleTimeString('en-GB');
    // console.log(element.Time);
    return newElement;
  });
  console.log(newTS);
  // console.log("asdf");

  // timeSeries.forEach((el) => {
  //   console.log(el.Time + " " + el.Value);
  //   let temp = new Date(el.Time * 1000);
  //   // console.log(temp.toLocaleTimeString('en-GB'))
  //   el.Time = temp.toLocaleTimeString('en-GB');
  //   console.log(el.Time);
  //   // console.log(`${temp.getHours()}:${temp.getMinutes().length == 1 ? "0" + temp.getMinutes() : temp.getMinutes()}:${temp.getSeconds()}`);
  // });
return (
<LineChart width={730} height={500} data={timeSeries}
  margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
  <CartesianGrid strokeDasharray="3 3" />
  <XAxis dataKey="Time" />
  <YAxis label={{ value: data_name, angle: -90, position: 'insideLeft' }}/>
  <XAxis label={{ value: 'Time', offset: -5, position: 'insideBottom' }}/>
  <Tooltip/>
  <Line type="monotone" dataKey="Value" stroke="#8884d8" />
</LineChart>
);
}
export default Chart;