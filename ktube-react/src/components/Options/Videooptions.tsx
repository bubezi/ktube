import "bootstrap";
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap/dist/js/bootstrap.js";

import { elipsisStyle, toggleStyle } from "../../assets/styles/Styles";

import Dropdown from "react-bootstrap/Dropdown";
import Playlistoption from "./Playlistoption";
import Watchlateroption from "./Watchlateroption";
import { useViewerContext } from "../../providers/ViewerProvider";
import { usePlaylistsContext } from "../../providers/PlaylistsProvider";

interface PropOptions {
  videoId: number;
}

const Videooptions = (props: PropOptions) => {
  const playlists = usePlaylistsContext().playlists;
  const watchlater = usePlaylistsContext().watchlater;
  const myToken = useViewerContext().myToken;

  if (myToken) {
    if (!Array.isArray(playlists)) {
      return null; // or handle the error in an appropriate way
    } else {
      const playlistoptions = playlists.map((playlist) => {
        if (playlist.id !== 0) {
          const playlistId = Number(playlist.id);

          if (playlist.videos.includes(props.videoId)) {
            const prompt = `Remove Video from ${playlist.name}`;
            return (
              <Playlistoption
                key={playlistId}
                name={playlist.name}
                prompt={prompt}
                playlistId={playlistId}
                videoId={props.videoId}
                add={false}
                itemId={"playlist-" + playlistId + "-video-" + props.videoId}
                myToken={myToken}
              />
            );
          } else {
            const prompt = `Add Video to ${playlist.name}`;
            return (
              <Playlistoption
                key={playlistId}
                name={playlist.name}
                prompt={prompt}
                playlistId={playlistId}
                videoId={props.videoId}
                add={true}
                itemId={"playlist-" + playlistId + "-video-" + props.videoId}
                myToken={myToken}
              />
            );
          }
        }
      });

      const watchlaterOption = watchlater.map((watchlaterItem) => {
        const playlistId = Number(watchlaterItem.id);
        if (watchlaterItem.videos.includes(props.videoId)) {
          const playlistName = "Remove Video from Watchlater";
          return (
            <Watchlateroption
              key={playlistId}
              prompt={playlistName}
              videoId={props.videoId}
              add={false}
              itemId={"watchlater-" + playlistId + "-video-" + props.videoId}
              myToken={myToken}
            />
          );
        } else {
          const playlistName = "Add Video to Watchlater";
          return (
            <Watchlateroption
              key={playlistId}
              prompt={playlistName}
              videoId={props.videoId}
              add={true}
              itemId={"watchlater-" + playlistId + "-video-" + props.videoId}
              myToken={myToken}
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
