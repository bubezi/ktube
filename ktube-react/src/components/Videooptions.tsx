import "bootstrap";
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap/dist/js/bootstrap.js";

import React from "react";
import axios from "axios";
import { API_URL } from "../constants";
import Dropdown from "react-bootstrap/Dropdown";

import { handleAddToPlaylist, handleRemoveFromPlaylist } from "../functions/fun";

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
  color: "black",
};

interface PropOption {
  playlistName: string;
  playlistId: number;
  videoId: number;
  add: boolean;
  itemId: string;
}


function Option(props: PropOption) {
  let handleClick = (event: any) => {console.log(event)};

  if (props.add){
    handleClick = (event)=>{
      handleAddToPlaylist(event, props.videoId, props.playlistId);
    }
  }else{
    handleClick = (event)=>{
      handleRemoveFromPlaylist(event, props.videoId, props.playlistId);
    }
  }
  return (
    <Dropdown.Item style={optionsStyle} id={props.itemId} href="#" onClick={handleClick}>
      {props.playlistName}
    </Dropdown.Item>
  );
}

interface Playlist {
  id: number;
  name: string;
  videos: Array<number>;
}

interface PropOptions {
  videoId: number;
  slug: string;
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
          const playlistId = Number(playlist.id);

          if (playlist.videos.includes(props.videoId)) {
            const playlistName = `Remove Video from ${playlist.name}`;
            return (
              <Option
                key={playlistId}
                playlistName={playlistName}
                playlistId={playlistId}
                videoId={props.videoId}
                add={false}
                itemId={"playlist-" + playlistId + "-video-" + props.videoId}
              />
            );
          } else {
            const playlistName = `Add Video to ${playlist.name}`;
            return (
              <Option
                key={playlistId}
                playlistName={playlistName}
                playlistId={playlistId}
                videoId={props.videoId}
                add={true}
                itemId={"playlist-" + playlistId + "-video-" + props.videoId}
              />
            );
          }
        }
      });

      return (
        <>
          <div className="video-options">
            <div className="dropdown">
              <Dropdown>
                <Dropdown.Toggle
                  id="dropdownMenuButton"
                  className="custom-dropdown"
                  style={toggleStyle}
                >
                  <i
                    className="fa-solid fa-ellipsis-vertical"
                    style={elipsisStyle}
                  ></i>
                </Dropdown.Toggle>

                <Dropdown.Menu>{playlistoptions}</Dropdown.Menu>
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
              <Dropdown.Toggle
                id="dropdownMenuButton"
                className="custom-dropdown"
                style={toggleStyle}
              >
                <i
                  className="fa-solid fa-ellipsis-vertical"
                  style={elipsisStyle}
                ></i>
              </Dropdown.Toggle>

              <Dropdown.Menu>
                <Dropdown.Item href="/auth/login">
                  Add to Playlist
                </Dropdown.Item>
                <Dropdown.Item href="/auth/login">
                  Add to Watchlater
                </Dropdown.Item>
              </Dropdown.Menu>
            </Dropdown>
          </div>
        </div>
      </>
    );
  }
}

export default Videooptions;
