// import './App.css'
import "bootstrap/dist/css/bootstrap.css";

// import { Routes, Route, Link } from "react-router-dom";
import Homepage from './components/Homepage';
// import Watchpage from "./components/Watchpage";


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
      <Homepage/>
    </div>
    </>
  )
}

export default App
