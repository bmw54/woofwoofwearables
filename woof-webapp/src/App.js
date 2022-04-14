import './App.css';
import React, { useState, useEffect } from 'react';
import 'bootstrap/dist/css/bootstrap.css'
import { Nav } from 'react-bootstrap'
import { Link, Outlet } from "react-router-dom"
import { LinkContainer } from 'react-router-bootstrap'
import ChartColoredFlag from './chartColoredFlag';
import WoofLineChart from './woofLineChart';
import WoofBarChart from './woofBarChart';


function App() {
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
      <WoofLineChart data_name={"test"} />
      <WoofBarChart />

      <Outlet />
    </div>
  );
}

export default App;
