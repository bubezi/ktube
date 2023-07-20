import React from "react";
import axios from "axios";
import { API_URL } from "../constants";

// import { handleAddToPlaylist } from "../functions/fun";

const optionsStyle = {
  display: 'block'
}

interface PropOptions {
  videoId:number,
  slug:string
}

interface PropOption {
  playlistName: string,
  playlistId: number,
  videoId: number
}

function Option(props:PropOption) {
  const itemId: string = "playlist-"+props.playlistId+"-video-"+props.videoId
  return (<a 
          className="dropdown-item add-btn-link update-cart" 
          style={optionsStyle}
          id={itemId}
          >Add video to {props.playlistName}</a>
          );
}


interface Playlist {
  id: number,
  name:string,
}

const playlistsInit:Array<Playlist> = [{id: 0, name:''}]

function Videooptions(props:PropOptions) {
  const [playlists, setPlaylists] = React.useState<Array<Playlist>>(playlistsInit);
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
        .then((res) => setPlaylists(res.data))
        .catch((error) => {
          console.log(error);
        });
    }, []);

    const playlistOptions = playlists.map(playlist => {
        console.log(playlist);

        return (<Option 
                  key={playlist.id} 
                  playlistName={playlist.name} 
                  videoId={props.videoId} 
                  playlistId={playlist.id}/>
        );
    });

    return (
      <>
        <div className="video-options">
          <div className="dropdown">
            <button
              className="btn"
              type="button"
              id="dropdownMenuButton"
              data-toggle="dropdown"
              aria-haspopup="true"
              aria-expanded="true"
            >
              <i className="fa-solid fa-ellipsis-vertical"></i>
            </button>
            <div className="dropdown-menu dropdown-menu-right" aria-labelledby="dropdownMenuButton">
            {playlistOptions}
            </div>
          </div>
        </div>
      </>
    );
  } else {
    return (
      <>
        <div className="video-options">
          <div className="dropdown">
            <button
              className="btn"
              type="button"
              id="dropdownMenuButton"
              data-toggle="dropdown"
              aria-haspopup="true"
              aria-expanded="true"
            >
              <i className="fa-solid fa-ellipsis-vertical"></i>
            </button>
            <div
              className="dropdown-menu dropdown-menu-right"
              aria-labelledby="dropdownMenuButton"
            >
              <a href="/auth/login" className="dropdown-item add-btn-link update-cart" 
                style={optionsStyle}
                >Add to playlist</a>
            </div>
          </div>
        </div>
      </>
    );
  }
}

export default Videooptions;
