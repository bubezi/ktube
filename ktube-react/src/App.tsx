
import "bootstrap/dist/css/bootstrap.min.css";

import { BrowserRouter, Routes, Route } from "react-router-dom";

import Homepage from './components/Homepage';
import Loader from "./components/Loader";
import Auth from "./components/Auth/Auth";
import Navbar from "./components/Navbar";
import ViewerProvider from "./providers/ViewerProvider";
import Watchpage from "./components/Watchpage";
import PlaylistProvider from "./providers/PlaylistsProvider";
import Channel from "./components/Channel";
import Playlist from "./components/Playlist";


function App() {

  return (
    <>
      <Loader />
      <ViewerProvider>
      <PlaylistProvider>
        <Navbar/>
          <BrowserRouter>
            <Routes>
              <Route path="/" element={<Homepage />} />
              <Route path="/auth/login" element={<Auth />} />
              <Route path="/watch/:slug" element={<Watchpage/>} />
              <Route path="/channel/:channelId" element={<Channel/>} />
              <Route path="/playlist/:playlistId" element={<Playlist/>} />
            </Routes>
          </BrowserRouter>
      </PlaylistProvider>
      </ViewerProvider>
    </>
  )
}

export default App;
