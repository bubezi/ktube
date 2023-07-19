import React from "react";
import axios from "axios";
import { API_URL } from "../constants";

interface Playlist {
    name:string,
}

const playlistsInit:Array<Playlist> = [{name:''}]
function Videooptions() {
  const [playlists, setPlaylists] = React.useState<Array<Playlist>>(playlistsInit);
  const [myToken] = React.useState(() => {
    const savedToken = localStorage.getItem("token");
    return savedToken ?? null;
  });

  const optionsStyle = {
    display: 'block'
  }

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

    const options = playlists.map(playlist => {

        return (
            <form id="remove-video-{{video.slug}}-from-watchlater-form">
                {/* {% csrf_token %} */}
                <input type="hidden" name="video_id" value="{{video.slug}}"/>
                <a href="#" className="dropdown-item add-btn-link update-cart" 
                id="remove-video-{{video.slug}}-from-watchlater-button" 
                style={optionsStyle}
                >{playlist.name}</a>
            </form>
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
            {options}
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
            <form id="remove-video-{{video.slug}}-from-watchlater-form">
                {/* {% csrf_token %} */}
                <input type="hidden" name="video_id" value="{{video.slug}}"/>
                <a href="#" className="dropdown-item add-btn-link update-cart" 
                id="remove-video-{{video.slug}}-from-watchlater-button" 
                style={optionsStyle}
                >Remove Video From Watchlater</a>
            </form>
            </div>
          </div>
        </div>
      </>
    );
  }
}

export default Videooptions;
