import React, { useState, useEffect } from 'react';
import 'bootstrap/dist/css/bootstrap.css'
import WoofLineChart from '../woofLineChart';
import WoofBarChart from '../woofBarChart';
import axios from 'axios'
import { Container, Row, Col, ToggleButtonGroup } from 'react-bootstrap';
import { ToggleButton } from 'react-bootstrap';

let windowNum = 0;

export default function Trends() {
  const [frequencyData, setFrequencyData] = useState([]);
  const [anglesData, setAnglesData] = useState([]);
  const [pitchesData, setPitchesData] = useState([]);
  const [amplitudeData, setAmplitudeData] = useState([]);
  const [sideBiasData, setSideBiasData] = useState([]);
  const [radioValue, setRadioValue] = useState(1);
  const [moodData, setMoodData] = useState();


  const radios = [
    { name: 'Today', value: 1 },
    { name: 'Week', value: 2 },
    { name: 'Month', value: 3 },
    { name: 'Year', value: 4 },
  ];

  let mood = [];
  let sideBias = [];
  let amplitude = [];
  let frequency = [];

  let moodMap = new Map();






  useEffect(() => {
    let interval
    moodMap.set("excited", <span role="img" aria-label="excited">😝</span>);
    moodMap.set("happy", <span role="img" aria-label="happy">😀</span>);
    moodMap.set("idle", <span role="img" aria-label="idle">😐</span>);
    moodMap.set("sad", <span role="img" aria-label="sad">🙁</span>);
    // console.log(moodMap.get("sad"));

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

      axios.get('http://localhost:5000/spreadsheet/angles/' + windowNum).then(response => {
        console.log("SUCCESS", response.data)
        setAnglesData(response.data)
      }).catch(error => {
        console.log(error)
      })

      axios.get('http://localhost:5000/spreadsheet/mood/' + windowNum).then(response => {
        console.log("SUCCESS", response.data)
        console.log("ASDFAD ", response.data[0]);
        mood = mood.concat(response.data[0])
        setMoodData(response.data[0].Value)
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
    <main>
      <h1>Trends</h1>
      <div style={{ marginBottom: "30px" }}>Fido is currently feeling <strong>{moodData}</strong>{moodData ? moodMap.get(moodData.toLowerCase()) : ""}</div>
      <ToggleButtonGroup type="radio" defaultValue={1} name="dateRadio" onChange={(e) => setRadioValue(e)}>
        {radios.map((radio, idx) => (
          <ToggleButton
            key={idx}
            id={`radio-${idx}`}
            type="radio"
            variant='outline-primary'
            name="radio"
            value={radio.value}
            checked={radioValue === radio.value}
          >
            {radio.name}
          </ToggleButton>
        ))}
      </ToggleButtonGroup>
      <br />

      <Container>
        <Row>
          <Col></Col>
        </Row>
        <Row>
          <Col xs={6}>
            <WoofLineChart data_name={"Angles"} timeseries={anglesData} yLabel="Degrees" xLabel='Seconds' />
            <br />
            <WoofLineChart data_name={"Pitches"} timeseries={pitchesData} yLabel="Degrees" xLabel='Seconds' />
          </Col>
          <Col xs={6}>
            <WoofLineChart data_name={"Frequency"} timeseries={frequencyData} xLabel="Time" yLabel="Frequency (Wags per second)" yFontSize={14} yPosition="insideBottomLeft" />
            <br />
            <WoofLineChart data_name={"Amplitude"} timeseries={amplitudeData} xLabel="Time" yLabel="Amplitude (Degrees)" yFontSize={14} yPosition="insideBottomLeft" />
          </Col>
        </Row>
        <br />
        <Row>
          <Col xs={6}>
            <WoofBarChart data_name={"Side Bias"} timeseries={sideBiasData} />
          </Col>

        </Row>
      </Container>

    </main >
  );
}