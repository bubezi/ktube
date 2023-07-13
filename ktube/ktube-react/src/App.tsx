// import './App.css'
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap/dist/css/bootstrap.min.css";

import Homepage from './components/Homepage';
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";


function App() {

  return (
    <>
    <div className="App">
      <Navbar username="Bubezi"/>
      <div className="container">
        <Homepage/>
      </div>
      <Footer/>
    </div>
    </>
  )
}

export default App