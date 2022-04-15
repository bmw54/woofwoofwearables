import { Row, Container, Col } from 'react-bootstrap';

//all 4 params are arrays accel, gyro, magnetic, angle
function Home({data}){

  return (
    <Container>
      <h2>Frequency</h2>
      <Row style={{marginBottom: "1em"}}>
        <Col xs={4}>x: {data.Frequency}</Col>
      </Row>
      <h2>Amplitude</h2>
      <Row style={{marginBottom: "1em"}}>
        <Col xs={4}>x: {data.Amplitude}</Col>
      </Row>
      <h2>Mood</h2>
      <Row style={{marginBottom: "1em"}}>
        <Col xs={4}>x: {data.Mood}</Col>
      </Row>
      <h2>Image-Url</h2>
      <Row style={{marginBottom: "1em"}}>
        <Col xs={4}>x: {data.ImageUrl}</Col>
      </Row>
    </Container>
  );
}

export default Home;