// import './App.css'
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap/dist/css/bootstrap.min.css";

// import { Routes, Route, Link } from "react-router-dom";
import Homepage from './components/Homepage';
// import Watchpage from "./components/Watchpage";
import Navbar from "./components/Navbar";


function App() {

  return (
    <>
    <div className="App">
      {/* <nav className="navbar"> */}
        {/* <Link to="/" className="nav-item">Homepage</Link> */}
        {/* <Link to="/" className="nav-item">Watchpage</Link> */}
      {/* </nav> */}
      {/* <Routes> */}
        {/* <Route path="/watch" element={<Watchpage/>}/> */}
        {/* <Route path="/" element={<Homepage/>}/> */}
      {/* </Routes> */}
      <Navbar username="Bubezi"/>
      <Homepage/>
    </div>
    </>
  )
}

export default App
