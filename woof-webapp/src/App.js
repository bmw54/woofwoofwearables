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
import { Grid, GridSpan } from '@react-ui-org/react-ui';
import WoofMoodDisplay from './WoofMoodDisplay';
import { useLocation } from 'react-router-dom';
import Home from "./routes/home"


let windowNum = 0;


function App() {
  let location = useLocation();
  // console.log(location)
  const [frequencyData, setFrequencyData] = useState([]);
  const [anglesData, setAnglesData] = useState([]);
  const [pitchesData, setPitchesData] = useState([]);
  const [amplitudeData, setAmplitudeData] = useState([]);
  const [sideBiasData, setSideBiasData] = useState([]);
  const [moodData, setMoodData] = useState([]);
  const [imageUrl, setImageUrl] = useState([]);

  let mood = [];
  let sideBias = [];
  let amplitude = [];
  let frequency = [];


  useEffect(() => {
    let interval

    const fetchData = async () => {
      axios.get('http://localhost:5000/spreadsheet/frequency/' + windowNum).then(response => {
        console.log("SUCCESS", response.data)
        frequency = frequency.concat(response.data[0])
        setFrequencyData(frequency)
      }).catch(error => {
        console.log(error)
      })

      axios.get('http://localhost:5000/spreadsheet/amplitude/' + windowNum).then(response => {
        console.log("SUCCESS", response.data)
        amplitude = amplitude.concat(response.data[0])
        setAmplitudeData(amplitude)
      }).catch(error => {
        console.log(error)
      })

      axios.get('http://localhost:5000/spreadsheet/sidebias/' + windowNum).then(response => {
        console.log("SUCCESS", response.data)
        sideBias = sideBias.concat(response.data[0])
        setSideBiasData(sideBias)
      }).catch(error => {
        console.log(error)
      })

      axios.get('http://localhost:5000/spreadsheet/mood/' + windowNum).then(response => {
        console.log("SUCCESS", response.data)
        mood = mood.concat(response.data[0])
        setMoodData(mood)
      }).catch(error => {
        console.log(error)
      })

      axios.get('http://localhost:5000/spreadsheet/happyphoto/' + windowNum).then(response => {
        console.log("SUCCESS", response.data)
        setImageUrl(response.data)
      }).catch(error => {
        console.log(error)
      })

      axios.get('http://localhost:5000/spreadsheet/angles/' + windowNum).then(response => {
        console.log("SUCCESS", response.data)
        setAnglesData(response.data)
      }).catch(error => {
        console.log(error)
      })

      axios.get('http://localhost:5000/spreadsheet/pitches/' + windowNum).then(response => {
        console.log("SUCCESS", response.data)
        setPitchesData(response.data)
      }).catch(error => {
        console.log(error)
      })
      if (windowNum >= 8) {
        clearInterval(interval);
      } else {
        windowNum++;
      }

    }
    interval = setInterval(() => {
      fetchData()
    }, 10 * 1000)

  }, [])

  return (
    <div className='app'>
      <div className="sidebar">
        <h2>PupSmart</h2>
        <Nav variant="pills" defaultActiveKey="/home" className="flex-column sidenav">
          <LinkContainer to="/"><Nav.Link>Home</Nav.Link></LinkContainer>
          <LinkContainer to="/trends"><Nav.Link>Trends</Nav.Link></LinkContainer>
          <LinkContainer to="/livestream"><Nav.Link>Livestream</Nav.Link></LinkContainer>
          <LinkContainer to="/logs"><Nav.Link>Logs</Nav.Link></LinkContainer>
        </Nav>
        <div>Profile</div>
      </div>
      {location.pathname == "/" ? <Home /> : <Outlet />}
    </div>
  );
}

export default App;
