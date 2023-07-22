import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap/dist/js/bootstrap.js';
// import $ from 'jquery';
// import Popper from 'popper.js';


import React from "react";
import axios from "axios";
import { API_URL } from "../constants";
import Dropdown from 'react-bootstrap/Dropdown';


const optionsStyle = {
  display: "block",
};

const toggleStyle = {
  padding: 0,
  outline: 0,
  border: "none",
  backgroundColor: "white",
};

const elipsisStyle = {
  color:"black",
};

interface PropOptions {
  videoId: number;
  slug: string;
}

interface PropOption {
  playlistName: string;
  playlistId: number;
  videoId: number;
}

function Option(props: PropOption) {

  const itemId: string =
    "playlist-" + props.playlistId + "-video-" + props.videoId;
  return (
    <Dropdown.Item 
      style={optionsStyle}
      id={itemId}
      href="#">{props.playlistName}</Dropdown.Item>
  );
}

interface Playlist {
  id: number;
  name: string;
}

function Videooptions(props: PropOptions) {
  const [playlists, setPlaylists] = React.useState<Array<Playlist>>([]);
  const [myToken] = React.useState(() => {
    const savedToken = localStorage.getItem("token");
    return savedToken ?? null;
  });

  if (myToken) {
    React.useEffect(() => {
      axios({
        method: "get",
        url: API_URL + "playlistsHome",
        headers: {
          Authorization: `Token ${myToken}`,
        },
      })
        .then((res) => {
          if (Array.isArray(res.data.playlists)) {
            setPlaylists(res.data.playlists);
          } else {
            // handle error
          }
        })
        .catch((error) => {
          console.log(error);
        });
    }, []);

    if (!Array.isArray(playlists)) {
      return null; // or handle the error in an appropriate way
    } else {
      const playlistoptions = playlists.map((playlist) => {
        if (playlist.id !== 0) {
          const playlistName = `${playlist.name}`;
          const playlistId = Number(playlist.id);

          return (
            <Option
              key={playlistId}
              playlistName={playlistName}
              playlistId={playlistId}
              videoId={props.videoId}
            />
          );
        }
      });

      return (
        <>
        <div className="video-options">
            <div className="dropdown">
              <Dropdown>
                <Dropdown.Toggle id="dropdownMenuButton" className="custom-dropdown" style={toggleStyle}>
                  <i className="fa-solid fa-ellipsis-vertical" style={elipsisStyle}></i>
                </Dropdown.Toggle>
          
                <Dropdown.Menu>
                  {playlistoptions}
                </Dropdown.Menu>
              </Dropdown>
            </div>
        </div>
        </>
      );
    }
  } else {
    return (
      <>
      <div className="video-options">
          <div className="dropdown">
            <Dropdown>
              <Dropdown.Toggle id="dropdownMenuButton" className="custom-dropdown" style={toggleStyle}>
                <i className="fa-solid fa-ellipsis-vertical" style={elipsisStyle}></i>
              </Dropdown.Toggle>
        
              <Dropdown.Menu>
                <Dropdown.Item href="/auth/login">Add to playlist</Dropdown.Item>
              </Dropdown.Menu>
            </Dropdown>
          </div>
      </div>
      </>
    );
  }
}

export default Videooptions;
