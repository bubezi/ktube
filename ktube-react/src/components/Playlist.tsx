import axios from "axios";
import React from "react";
import { useParams } from "react-router-dom";
import { API_URL } from "../constants";
import { VideoType } from "./Videos";
import { paddingTop35 } from "../assets/styles/WatchStyles";
import Playlistcard from "./Playlistcard";
import { PlaylistChannel } from "./Channel";
import Playlistvideocard from "./Playlistvideocard";

const playlistInit = {
  id: 0,
  name: "",
  views: 0,
  public: false,
  created_on: "",
  channel: "",
  videos: [],
};

const Playlist = () => {
  const { playlistId } = useParams();
  const [playlist, setPlaylist] = React.useState<PlaylistChannel>(playlistInit);
  const [videos, setVideos] = React.useState<Array<VideoType>>([]);

  React.useEffect(() => {
    if (Number(playlistId) !== 0) {
      axios({
        method: "get",
        url: API_URL + "playlistAPI/" + playlistId,
      })
        .then((res) => {
          setPlaylist(res.data);
        })
        .catch((error) => {
          console.log(error);
        });

      axios({
        method: "get",
        url: API_URL + "playlistVideosAPI/" + playlistId,
      })
        .then((res) => {
          setVideos(res.data);
        })
        .catch((error) => {
          console.log(error);
        });
    }
  }, [playlistId]);

  React.useEffect(() => {
    document.title = playlist.name + " | KTUBE";
  }, [playlist]);

  const showVideos = videos.map((video) => {
    return <Playlistvideocard key={video.id} video={video} />;
  });

  return (
    <>
      <div className="container" style={paddingTop35}>
        <div className="row">
          <Playlistcard playlist={playlist} colSize="12" />
        </div>
        <div className="row">
          <div className="col-lg-2">
            <a href={"/watchplaylist/" + playlist.id}>
              <button className="btn btn-success">Watch Playlist</button>
            </a>
          </div>
        </div>
        <div className="row">{showVideos}</div>
      </div>
    </>
  );
};

export default Playlist;
