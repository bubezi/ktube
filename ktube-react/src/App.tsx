
import "bootstrap/dist/css/bootstrap.min.css";

import { BrowserRouter, Routes, Route } from "react-router-dom";

import Homepage from './components/Homepage';
import Loader from "./components/Loader";
// import Watchpage from "./components/Watchpage";


function App() {

  return (
    <>
      <Loader />
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Homepage />} />
        </Routes>
      </BrowserRouter>
    </>
  )
}

export default App;
