import "bootstrap";
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap/dist/js/bootstrap.js";

import React from "react";
import axios from "axios";
import { API_URL } from "../constants";
import Dropdown from "react-bootstrap/Dropdown";
import Option from "./Options";

import {
  handleAddToPlaylist,
  handleAddToWatchlater,
  handleRemoveFromPlaylist,
  handleRemoveFromWatchlater,
} from "../functions/fun";

import { toggleStyle, elipsisStyle } from "./styles/Styles";

interface Playlist {
  id: number;
  name: string;
  videos: Array<number>;
}

interface Watchlater {
  id: number;
  videos: Array<number>;
}

interface PropOptions {
  videoId: number;
  slug: string;
}

function Videooptions(props: PropOptions) {
  const [playlists, setPlaylists] = React.useState<Array<Playlist>>([]);
  const [watchlater, setWatchlater] = React.useState<Array<Watchlater>>([]);
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
                handleMethod={async () => handleRemoveFromPlaylist(
                  props.videoId,
                  playlistId,
                  myToken
                )}
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
                handleMethod={async () => handleAddToPlaylist(
                  props.videoId,
                  playlistId,
                  myToken
                )}
              />
            );
          }
        }
      });

      React.useEffect(() => {
        axios({
          method: "get",
          url: API_URL + "watchlater",
          headers: {
            Authorization: `Token ${myToken}`,
          },
        })
          .then((res) => {
            if (Array.isArray(res.data.watchlater)) {
              setWatchlater(res.data.watchlater);
            } else {
              setWatchlater(Array(res.data.watchlater));
            }
          })
          .catch((error) => {
            console.log(error);
          });
      }, []);

      const watchlaterOption = watchlater.map((watchlaterItem) => {
        const playlistId = Number(watchlaterItem.id);
        if (watchlaterItem.videos.includes(props.videoId)) {
          const playlistName = "Remove Video from Watchlater";
          return (
            <Option
              key={playlistId}
              playlistName={playlistName}
              playlistId={playlistId}
              videoId={props.videoId}
              add={false}
              itemId={"watchlater-" + playlistId + "-video-" + props.videoId}
              handleMethod={async () => handleRemoveFromWatchlater(props.videoId, myToken)}
            />
          );
        } else {
          const playlistName = "Add Video to Watchlater";
          return (
            <Option
              key={playlistId}
              playlistName={playlistName}
              playlistId={playlistId}
              videoId={props.videoId}
              add={true}
              itemId={"watchlater-" + playlistId + "-video-" + props.videoId}
              handleMethod={async () => handleAddToWatchlater(props.videoId, myToken)}
            />
          );
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
                <Dropdown.Menu>
                  {playlistoptions}
                  {watchlaterOption}
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
