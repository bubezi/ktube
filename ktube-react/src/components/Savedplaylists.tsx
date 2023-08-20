import axios from "axios";
import React from "react";
import { API_URL } from "../constants";
import { useViewerContext } from "../providers/ViewerProvider";
import { PlaylistChannel } from "./Channel";
import Playlistcard from "./Playlistcard";

const Savedplaylists = () => {
    const myToken = useViewerContext().myToken;
    const [savedPlaylists, setSavedPlaylists] = React.useState<PlaylistChannel[]>([]);
  
    if (myToken) {
      document.title = "My Saved Playlists | KTUBE";
  
      React.useEffect(() => {
  
          axios({
            method: "get",
            url: API_URL + "savedPlaylists2API",
            headers: {
              Authorization: `Token ${myToken}`,
            },
          })
            .then((res) => {
              if (Array.isArray(res.data.savedPlaylists)) {
                setSavedPlaylists(res.data.savedPlaylists);
              } else {
                setSavedPlaylists(Array(res.data.savedPlaylists));
              }
            })
            .catch((error) => {
              console.log(error);
            });
  
      }, [myToken]);

      const MySavedPlaylists = () => {
        const pluralSavedPlaylists =
        savedPlaylists.length === 1 ? "playlist" : "playlists";
  
        const showSavedPlaylists = savedPlaylists.map((playlist) => {
          return (<Playlistcard key={playlist.id} colSize="4" playlist={playlist}/>);
        });
  
        return (
        <>
          <div className="row box-element">
            <div className="col-lg-12">
              <div className="row">
                <h3>My Saved Playlists - {savedPlaylists.length} {pluralSavedPlaylists}</h3>
              </div>
            </div>
          </div>
            <div className="row">{showSavedPlaylists}</div>
        </>
        );
      }
  
      return (
        <>
          <div className="container">
            <MySavedPlaylists/>
          </div>
        </>
      );
    } else {
      location.assign("/auth/login");
    }

}

export default Savedplaylists;
