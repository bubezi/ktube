
import "bootstrap/dist/css/bootstrap.min.css";

import { BrowserRouter, Routes, Route } from "react-router-dom";

import Homepage from './components/Homepage';
import Loader from "./components/Loader";
import Auth from "./components/Auth/Auth";
import Navbar from "./components/Navbar";
import ViewerProvider from "./providers/ViewerProvider";
import Watchpage from "./components/Watchpage";
import Watchplaylist from "./components/Watchplaylist";
import PlaylistProvider from "./providers/PlaylistsProvider";
import Channel from "./components/Channel";
import Playlist from "./components/Playlist";
import Library from "./components/Library";
import Watchlater from "./components/Watchlater";
import Savedplaylists from "./components/Savedplaylists";


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
              <Route path="/library" element={<Library />} />
              <Route path="/watchlater" element={<Watchlater />} />
              <Route path="/savedplaylists" element={<Savedplaylists />} />
              <Route path="/auth/login" element={<Auth />} />
              <Route path="/watch/:slug" element={<Watchpage/>} />
              <Route path="/channel/:channelId" element={<Channel/>} />
              <Route path="/playlist/:playlistId" element={<Playlist/>} />
              <Route path="/watchplaylist/:playlistId/:positionN" element={<Watchplaylist/>} />
            </Routes>
          </BrowserRouter>
      </PlaylistProvider>
      </ViewerProvider>
    </>
  )
}

export default App;
