import { Row, Container, Col } from 'react-bootstrap';

//all 4 params are arrays accel, gyro, magnetic, angle
function Home({accel, gyro, mag, angle}){
  console.log(accel);
  console.log(gyro);
  console.log(mag);
  console.log(angle);
  
  return (
    <Container>
      <h2>Acceleration</h2>
      <Row style={{marginBottom: "1em"}}>
        <Col xs={4}>x: {accel[0]}</Col>
        <Col xs={4}>y: {accel[1]}</Col>
        <Col xs={4}>z: {accel[2]}</Col>
      </Row>
      <h2>Gyroscope</h2>
      <Row style={{marginBottom: "1em"}}>
        <Col xs={4}>x: {gyro[0]}</Col>
        <Col xs={4}>y: {gyro[1]}</Col>
        <Col xs={4}>z: {gyro[2]}</Col>
      </Row>
      <h2>Magnetic</h2>
      <Row style={{marginBottom: "1em"}}>
        <Col xs={4}>x: {mag[0]}</Col>
        <Col xs={4}>y: {mag[1]}</Col>
        <Col xs={4}>z: {mag[2]}</Col>
      </Row>
      <h2>Angle</h2>
      <Row style={{marginBottom: "1em"}}>
        <Col xs={4}>x: {angle[0]}</Col>
        <Col xs={4}>y: {angle[1]}</Col>
        <Col xs={4}>z: {angle[2]}</Col>
      </Row>
    </Container>
    
  );
}

export default Home;