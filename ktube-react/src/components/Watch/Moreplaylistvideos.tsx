import React from "react";
import { VideoType, videoInit } from "../Videos";
import axios from "axios";
import { API_URL } from "../../constants";
import MorePlaylistVideosCard from "./MorePlaylistVideosCard";
import { PlaylistChannel } from "../Channel";

interface Props {
  videoId: number;
  position: number;
  playlist: PlaylistChannel;
}

const Moreplaylistvideos = (props: Props) => {
  const [moreVideos, setMoreVideos] = React.useState<VideoType[]>(videoInit);

  React.useEffect(() => {
    if (props.videoId !== 0) {
      axios({
        method: "get",
        url:
          API_URL +
          "morePlaylistVideos/" +
          props.playlist.id +
          "/" +
          props.videoId, // Exclude the video in the id
        // headers: {
        //   Authorization: `Token ${myToken}`,
        // },
      })
        .then((res) => {
          setMoreVideos(res.data.videos);
        })
        .catch((error) => {
          console.log(error);
        });
    }
  }, [props.videoId]);

  const morevideos = moreVideos.map((video) => {
    if (video.id === props.videoId) {
      return (
          <MorePlaylistVideosCard
            key={video.id}
            videoId={video.id}
            title={video.title}
            thumbnail={video.thumbnail}
            channelId={video.channel}
            slug={video.slug}
            price={video.price}
            views={video.views}
            colSize={"col-lg-12"+" "+"box-element-highlight"}
            playlistId={props.playlist.id}
            position={moreVideos.indexOf(video)+1}
          />
      );
    } else {
      return (
        <MorePlaylistVideosCard
          key={video.id}
          videoId={video.id}
          title={video.title}
          thumbnail={video.thumbnail}
          channelId={video.channel}
          slug={video.slug}
          price={video.price}
          views={video.views}
          colSize="col-lg-12"
          playlistId={props.playlist.id}
          position={moreVideos.indexOf(video)+1}
        />
      );
    }
  });

  return (
    <>
      <div className="row box-element">
        <h4>{props.playlist.name} Playlist</h4>
      </div>
      <div className="row box-element" id="more-playlist-videos">
        {morevideos}
      </div>
    </>
  );
};

export default Moreplaylistvideos;
