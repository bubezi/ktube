import './App.css'
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap/dist/css/bootstrap.min.css";

import Homepage from './components/Homepage';
import Navbar from "./components/Navbar";


function App() {

  return (
    <>
    <div className="App">
      <Navbar username="Bubezi"/>
      <Homepage/>
    </div>
    </>
  )
}

export default App
