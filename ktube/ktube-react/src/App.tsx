// import './App.css'
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap/dist/css/bootstrap.min.css";

// import { Routes, Route } from "react-router-dom";

import Homepage from './components/Homepage';
import Loader from "./components/Loader";
// import Watchpage from "./components/Watchpage";


function App() {

  return (
    <>
      <Loader />
      <Homepage/>
    </>
  )
}

export default App