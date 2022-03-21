import './App.css';
import React, { useState, useEffect } from 'react';
import Home from './Home';
import Chart from './chart';
import 'bootstrap/dist/css/bootstrap.css';
import Image from 'react-bootstrap/Image'
import axios from 'axios'

function App() {

  const [accelData, setAccelData] = useState([]);
  const [gyroData, setGyroData] = useState([]);
  const [magData, setMagData] = useState([]);
  const [angleData, setAngleData] = useState([]);
  const [imageURL, setImageURL] = useState("");

  const [accelerationXTimeSeries, setAccelerationXTimeSeries] = useState([]);
  const [accelerationYTimeSeries, setAccelerationYTimeSeries] = useState([]);
  const [accelerationZTimeSeries, setAccelerationZTimeSeries] = useState([]);

  const [velocityXTimeSeries, setVelocityXTimeSeries] = useState([]);
  const [velocityYTimeSeries, setVelocityYTimeSeries] = useState([]);
  const [velocityZTimeSeries, setVelocityZTimeSeries] = useState([]);

  const [gyroXTimeSeries, setGyroXTimeSeries] = useState([]);
  const [gyroYTimeSeries, setGyroYTimeSeries] = useState([]);
  const [gyroZTimeSeries, setGyroZTimeSeries] = useState([]);

  const [magXTimeSeries, setMagXTimeSeries] = useState([]);
  const [magYTimeSeries, setMagYTimeSeries] = useState([]);
  const [magZTimeSeries, setMagZTimeSeries] = useState([]);

  const [angleXTimeSeries, setAngleXTimeSeries] = useState([]);
  const [angleYTimeSeries, setAngleYTimeSeries] = useState([]);
  const [angleZTimeSeries, setAngleZTimeSeries] = useState([]);

  useEffect(()=>{

    axios.get('http://localhost:5000/firebase/averages/FridayPuppyRun/accel/X').then(response => {
      console.log("SUCCESS", response.data)
      setAccelerationXTimeSeries(response.data)
    }).catch(error => {
      console.log(error)
    })

    axios.get('http://localhost:5000/firebase/averages/FridayPuppyRun/accel/Y').then(response => {
      console.log("SUCCESS", response.data)
      setAccelerationYTimeSeries(response.data)
    }).catch(error => {
      console.log(error)
    })

    axios.get('http://localhost:5000/firebase/averages/FridayPuppyRun/accel/Z').then(response => {
      console.log("SUCCESS", response.data)
      setAccelerationZTimeSeries(response.data)
    }).catch(error => {
      console.log(error)
    })

    axios.get('http://localhost:5000/firebase/velocity/FridayPuppyRun/accel/X').then(response => {
      console.log("SUCCESS", response.data)
      setVelocityXTimeSeries(response.data)
    }).catch(error => {
      console.log(error)
    })

    axios.get('http://localhost:5000/firebase/velocity/FridayPuppyRun/accel/Y').then(response => {
      console.log("SUCCESS", response.data)
      setVelocityYTimeSeries(response.data)
    }).catch(error => {
      console.log(error)
    })

    axios.get('http://localhost:5000/firebase/velocity/FridayPuppyRun/accel/Z').then(response => {
      console.log("SUCCESS", response.data)
      setVelocityZTimeSeries(response.data)
    }).catch(error => {
      console.log(error)
    })
    
    // axios.get('http://localhost:5000/firebase/FridayPuppyRun/accel/X').then(response => {
    //   console.log("SUCCESS", response.data)
    //   setAccelerationXTimeSeries(response.data)
    // }).catch(error => {
    //   console.log(error)
    // })

    // axios.get('http://localhost:5000/firebase/FridayPuppyRun/accel/Y').then(response => {
    //   console.log("SUCCESS", response.data)
    //   setAccelerationYTimeSeries(response.data)
    // }).catch(error => {
    //   console.log(error)
    // })

    // axios.get('http://localhost:5000/firebase/FridayPuppyRun/accel/Z').then(response => {
    //   console.log("SUCCESS", response.data)
    //   setAccelerationZTimeSeries(response.data)
    // }).catch(error => {
    //   console.log(error)
    // })

    axios.get('http://localhost:5000/firebase/FridayPuppyRun/gyro/X').then(response => {
      console.log("SUCCESS", response.data)
      setGyroXTimeSeries(response.data)
    }).catch(error => {
      console.log(error)
    })

    axios.get('http://localhost:5000/firebase/FridayPuppyRun/gyro/Y').then(response => {
      console.log("SUCCESS", response.data)
      setGyroYTimeSeries(response.data)
    }).catch(error => {
      console.log(error)
    })

    axios.get('http://localhost:5000/firebase/FridayPuppyRun/gyro/Z').then(response => {
      console.log("SUCCESS", response.data)
      setGyroZTimeSeries(response.data)
    }).catch(error => {
      console.log(error)
    })

    axios.get('http://localhost:5000/firebase/FridayPuppyRun/mag/X').then(response => {
      console.log("SUCCESS", response.data)
      setMagXTimeSeries(response.data)
    }).catch(error => {
      console.log(error)
    })

    axios.get('http://localhost:5000/firebase/FridayPuppyRun/mag/Y').then(response => {
      console.log("SUCCESS", response.data)
      setMagYTimeSeries(response.data)
    }).catch(error => {
      console.log(error)
    })

    axios.get('http://localhost:5000/firebase/FridayPuppyRun/mag/Z').then(response => {
      console.log("SUCCESS", response.data)
      setMagZTimeSeries(response.data)
    }).catch(error => {
      console.log(error)
    })

    axios.get('http://localhost:5000/firebase/images').then(response => {
      console.log("SUCCESS", response.data)
      setImageURL(response.data)
    }).catch(error => {
      console.log(error)
    })

    axios.get('http://localhost:5000/firebase/CurrentIMUData/0').then(response => {
      console.log("SUCCESS", response.data)
      setAccelData(response.data)
    }).catch(error => {
      console.log(error)
    })

    axios.get('http://localhost:5000/firebase/CurrentIMUData/1').then(response => {
      console.log("SUCCESS", response.data)
      setGyroData(response.data)
    }).catch(error => {
      console.log(error)
    })

    axios.get('http://localhost:5000/firebase/CurrentIMUData/2').then(response => {
      console.log("SUCCESS", response.data)
      setMagData(response.data)
    }).catch(error => {
      console.log(error)
    })

    axios.get('http://localhost:5000/firebase/CurrentIMUData/3').then(response => {
      console.log("SUCCESS", response.data)
      setAngleData(response.data)
    }).catch(error => {
      console.log(error)
    })

  }, [])
  
  
  return (
    <div className="App">
      <Home accel={accelData} gyro={gyroData} mag={magData} angle={angleData}/>
      <Image fluid src={imageURL} />
      <Chart timeSeries = {accelerationXTimeSeries} data_name = "Average Acceleration X"/>
      <Chart timeSeries = {accelerationYTimeSeries} data_name = "Average Acceleration Y" />
      <Chart timeSeries = {accelerationZTimeSeries} data_name = "Average Acceleration Z"/>

      <Chart timeSeries = {velocityXTimeSeries} data_name = "Average Velocity X"/>
      <Chart timeSeries = {velocityYTimeSeries} data_name = "Average Velocity Y" />
      <Chart timeSeries = {velocityZTimeSeries} data_name = "Average Velocity Z"/>
</div>
  );
}

export default App;
