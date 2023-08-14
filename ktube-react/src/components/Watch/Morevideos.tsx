import React from "react";
import { VideoType, videoInit } from "../Videos";
import axios from "axios";
import { API_URL } from "../../constants";
import MoreVideosCard from "./MoreVideosCard";

interface Props {
  videoId: number,
}

const Morevideos = (props: Props) => {
  const [moreVideos, setMoreVideos] = React.useState<VideoType[]>(videoInit);

  React.useEffect(()=>{
    if (props.videoId !== 0){
      axios({
        method: "get",
        url: API_URL + "moreVideos/" + props.videoId, // Exclude the video in the id
        // headers: {
        //   Authorization: `Token ${myToken}`,
        // },
      })
        .then((res) => {
          setMoreVideos(res.data.videos);
        })
        .catch((error) => {
          console.log(error);
        });}
  }, [props.videoId]);

  const morevideos = moreVideos.map((video) => {
    return (
      <MoreVideosCard
        key={video.id}
        videoId={video.id}
        title={video.title}
        thumbnail={video.thumbnail}
        channelId={video.channel}
        slug={video.slug}
        price={video.price}
        views={video.views}
        colSize="col-lg-12"
      />
    );
  });

  return (
    <>
      <div className="row box-element" id="more-videos">
        {morevideos}
      </div>
    </>
  );
}

export default Morevideos;
