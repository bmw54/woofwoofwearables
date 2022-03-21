import './App.css';
import React, { useState, useEffect } from 'react';
import Home from './Home';
import Chart from './chart';
import 'bootstrap/dist/css/bootstrap.css';
import firebaseConfig from './firebase';
import {ref, onValue, child} from "firebase/database";
import { initializeApp } from 'firebase/app';
import { getDatabase} from "firebase/database";
import Image from 'react-bootstrap/Image'




function App() {
  const imuDBPath = "CurrentIMUData/1-set/";
  const accelPath = imuDBPath + "/0";
  const gyroPath = imuDBPath + "/1";
  const magPath = imuDBPath + "/2";
  const anglePath = imuDBPath + "/3";
  const imagesPath = "images/1-set";


  const seriesPath = "CurrentIMUData/2-push"
  const accelSeriesPath = seriesPath + "/accel";
  // const gyroSeriesPath = seriesPath + "/gyro";
  // const magSeriesPath = seriesPath + "/mag";
  // const angleSeriesPath = seriesPath + "/angle";

  const [accelData, setAccelData] = useState([]);
  const [gyroData, setGyroData] = useState([]);
  const [magData, setMagData] = useState([]);
  const [angleData, setAngleData] = useState([]);
  const [imageURL, setImageURL] = useState("");

  const [accelerationXTimeSeries, setAccelerationXTimeSeries] = useState([]);
  const [accelerationYTimeSeries, setAccelerationYTimeSeries] = useState([]);
  const [accelerationZTimeSeries, setAccelerationZTimeSeries] = useState([]);

  // const [gyroXTimeSeries, setGyroXTimeSeries] = useState([]);
  // const [gyroYTimeSeries, setGyroYTimeSeries] = useState([]);
  // const [gyroZTimeSeries, setGyroZTimeSeries] = useState([]);

  // const [magXTimeSeries, setMagXTimeSeries] = useState([]);
  // const [magYTimeSeries, setMagYTimeSeries] = useState([]);
  // const [magZTimeSeries, setMagZTimeSeries] = useState([]);

  // const [angleXTimeSeries, setAngleXTimeSeries] = useState([]);
  // const [angleYTimeSeries, setAngleYTimeSeries] = useState([]);
  // const [angleZTimeSeries, setAngleZTimeSeries] = useState([]);

  // const db = getDatabase();
  useEffect(() => {
    const app = initializeApp(firebaseConfig);
    const db = getDatabase(app);

    const accelRef = ref(db, accelPath);
    onValue(accelRef, (snapshot) => {
      const data = snapshot.val();
      setAccelData(data);
    });

    const gyroRef = ref(db, gyroPath);
    onValue(gyroRef, (snapshot) => {
      const data = snapshot.val();
      setGyroData(data);
    });

    const magRef = ref(db, magPath);
    onValue(magRef, (snapshot) => {
      const data = snapshot.val();
      setMagData(data);
    });

    const angleRef = ref(db, anglePath);
    onValue(angleRef, (snapshot) => {
      const data = snapshot.val();
      setAngleData(data);
    });

    const imageRef = ref(db, imagesPath);
    onValue(imageRef, (snapshot) => {
      const data = snapshot.val();
      setImageURL(data);
    });

    const accelerationXSeriesRef = ref(db, accelSeriesPath + "/X");
    const accelerationYSeriesRef = ref(db, accelSeriesPath + "/Y");
    const accelerationZSeriesRef = ref(db, accelSeriesPath + "/Z");
    onValue(accelerationXSeriesRef, (snapshot) => {
      const data = snapshot.val();
      console.log(data);
      var values = Object.keys(data).map(function(key){
        return data[key];
      });
      setAccelerationXTimeSeries(values);
      console.log(values);
    });
    onValue(accelerationYSeriesRef, (snapshot) => {
      const data = snapshot.val();
      console.log(data);
      var values = Object.keys(data).map(function(key){
        return data[key];
      });
      setAccelerationYTimeSeries(values);
      console.log(values);
    });
    onValue(accelerationZSeriesRef, (snapshot) => {
      const data = snapshot.val();
      console.log(data);
      var values = Object.keys(data).map(function(key){
        return data[key];
      });
      setAccelerationZTimeSeries(values);
      console.log(values);
    });

  //   const gyroSeriesRef = ref(db, gyroSeriesPath);
  //   onValue(gyroSeriesRef, (snapshot) => {
  //     const data = snapshot.val();
  //     console.log(data);
  //     var values = Object.keys(data).map(function(key){
  //       return data[key];
  //     });
  //     setGyroTimeSeries(values);
  //     console.log(values);
  //   });

  //   const magSeriesRef = ref(db, magSeriesPath);
  //   onValue(magSeriesRef, (snapshot) => {
  //     const data = snapshot.val();
  //     console.log(data);
  //     var values = Object.keys(data).map(function(key){
  //       return data[key];
  //     });
  //     setMagTimeSeries(values);
  //     console.log(values);
  //   });

  //   const angleSeriesRef = ref(db, angleSeriesPath);
  //   onValue(angleSeriesRef, (snapshot) => {
  //     const data = snapshot.val();
  //     console.log(data);
  //     var values = Object.keys(data).map(function(key){
  //       return data[key];
  //     });
  //     setAngleTimeSeries(values);
  //     console.log(values);
  //   });
  }, []);
  
  
  return (
    <div className="App">
      <Home accel={accelData} gyro={gyroData} mag={magData} angle={angleData}/>
      <Image fluid src={imageURL} />
      <Chart timeSeries = {accelerationXTimeSeries} direction = "X"/>
      <Chart timeSeries = {accelerationYTimeSeries}direction = "Y" />
      <Chart timeSeries = {accelerationZTimeSeries} direction = "Z"/>
    </div>
  );
}

export default App;
