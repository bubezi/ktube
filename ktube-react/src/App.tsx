
import "bootstrap/dist/css/bootstrap.min.css";

import { BrowserRouter, Routes, Route } from "react-router-dom";

import Homepage from './components/Homepage';
import Loader from "./components/Loader";
import Auth from "./components/Auth/Auth";
import Navbar from "./components/Navbar";


function App() {

  return (
    <>
      <>
      <Loader />
      </>
      <>
      <Navbar username="Bubezi"/>
      </>
      <>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Homepage />} />
          <Route path="/auth/login" element={<Auth />} />
        </Routes>
      </BrowserRouter>
      </>
    </>
  )
}

export default App;
