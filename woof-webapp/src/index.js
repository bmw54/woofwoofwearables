import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import App1 from './App1';
import reportWebVitals from './reportWebVitals';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Trends from './routes/trends';
import Log from './routes/log';
import Logs from './routes/logs';

import Livestream from './routes/livestream';

ReactDOM.render(
  // <React.StrictMode>
  //   <App1 />
  // </React.StrictMode>,
  <BrowserRouter>
    <Routes>
      <Route path="/" element={
        <React.StrictMode>
          <App />
        </React.StrictMode>
      } >
        <Route path="trends" element={<Trends />} />
        <Route path="logs" element={<Logs />}>
          <Route path=":logId" element={<Log />} />
        </Route>
        <Route path="livestream" element={<Livestream />} />
        <Route
          path="*"
          element={
            <main style={{ padding: "1rem" }}>
              <p>There's nothing here!</p>
            </main>
          }
        />
      </Route>
    </Routes>

  </BrowserRouter>,
  document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
