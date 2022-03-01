import './App.css';
import React, { useState, useEffect } from 'react';
import Home from './Home';
import Chart from './chart';
import 'bootstrap/dist/css/bootstrap.css';
import firebaseConfig from './firebase';
import {ref, onValue } from "firebase/database";
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

  const [accelData, setAccelData] = useState([]);
  const [gyroData, setGyroData] = useState([]);
  const [magData, setMagData] = useState([]);
  const [angleData, setAngleData] = useState([]);
  const [imageURL, setImageURL] = useState("");

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
  }, []);
  
  
  return (
    <div className="App">
      <Home accel={accelData} gyro={gyroData} mag={magData} angle={angleData}/>
      <Image fluid src={imageURL} />
      <Chart/>
    </div>
  );
}

export default App;
