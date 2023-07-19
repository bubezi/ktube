
import "bootstrap/dist/css/bootstrap.min.css";

import { BrowserRouter, Routes, Route } from "react-router-dom";

import Homepage from './components/Homepage';
import Loader from "./components/Loader";
import Auth from "./components/Auth/Auth";
import Navbar from "./components/Navbar";
import ViewerProvider from "./providers/ViewerProvider";


function App() {

  return (
    <>
      <Loader />
      <ViewerProvider>
      <Navbar/>
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<Homepage />} />
            <Route path="/auth/login" element={<Auth />} />
          </Routes>
        </BrowserRouter>
      </ViewerProvider>
    </>
  )
}

export default App;
