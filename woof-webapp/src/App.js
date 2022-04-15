import './App.css';
import React, { useState, useEffect } from 'react';
import 'bootstrap/dist/css/bootstrap.css'
import { Nav } from 'react-bootstrap'
import { Link, Outlet } from "react-router-dom"
import { LinkContainer } from 'react-router-bootstrap'
import ChartColoredFlag from './chartColoredFlag';
import WoofLineChart from './woofLineChart';
import WoofBarChart from './woofBarChart';
import axios from 'axios'

let windowNum = 0;


function App() {

  const [frequencyData, setFrequencyData] = useState([]);
  const [anglesData, setAnglesData] = useState([]);
  const [pitchesData, setPitchesData] = useState([]);
  const [spreedsheetData, setSpreedsheetData] = useState([]);
  

  useEffect(()=>{
    let interval
  
    const fetchData = async () => {
      axios.get('http://localhost:5000/firebase/spreedsheet/' + windowNum).then(response => {
      console.log("SUCCESS", response.data)
      setSpreedsheetData(response.data)
      windowNum ++;
      }).catch(error => {
        console.log(error)
      })
     }  
     interval = setInterval(() => {
      fetchData()
    }, 10 * 1000)


    axios.get('http://localhost:5000/firebase/frequency/harnessrunzero/0').then(response => {
      console.log("SUCCESS", response.data)
      setFrequencyData(response.data)
    }).catch(error => {
      console.log(error)
    })

    axios.get('http://localhost:5000/firebase/angles/harnessrunzero/0').then(response => {
      console.log("SUCCESS", response.data)
      setAnglesData(response.data)
    }).catch(error => {
      console.log(error)
    })

    axios.get('http://localhost:5000/firebase/pitches/harnessrunzero/0').then(response => {
      console.log("SUCCESS", response.data)
      setPitchesData(response.data)
    }).catch(error => {
      console.log(error)
    })
  }, [])

  return (
    <div className='app'>
      {/* <nav
        style={{
          borderBottom: "solid 1px",
          paddingBottom: "1rem",
        }}
      >
        <Link to="/trends">Trends</Link> |{" "}
        <Link to="/livestream">Livestream</Link> |{" "}
        <Link to="/logs">Logs</Link>
      </nav> */}
      <div className="sidebar">
        <h1>PupSmart</h1>
        <Nav variant="pills" defaultActiveKey="/home" className="flex-column sidenav">
          <LinkContainer to="/"><Nav.Link>Home</Nav.Link></LinkContainer>
          <LinkContainer to="/trends"><Nav.Link>Trends</Nav.Link></LinkContainer>
          <LinkContainer to="/livestream"><Nav.Link>Livestream</Nav.Link></LinkContainer>
          <LinkContainer to="/logs"><Nav.Link>Logs</Nav.Link></LinkContainer>
        </Nav>
        <div>Profile</div>
      </div>
      {/* <ChartColoredFlag data_name={"test"} /> */}
      <WoofLineChart data_name={"Angles"} timeseries = {anglesData} />
      <WoofBarChart />
      <ul>
        {spreedsheetData.map((item) => (
          <li>{item.value}</li>
        ))}
      </ul>
      {/* <Home data = {spreedsheetData}/> */}
      <Outlet />
    </div>
  );
}

export default App;
