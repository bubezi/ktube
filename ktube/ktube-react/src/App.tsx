// import './App.css'
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap/dist/css/bootstrap.min.css";

import Homepage from './components/Homepage';
import Footer from "./components/Footer";
import Loader from "./components/Loader";


function App() {

  return (
    <>
    <Loader />
    <div className="App">
      <Homepage/>
      <Footer/>
    </div>
    </>
  )
}

export default App
