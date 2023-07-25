import React from "react";
import { VideoType } from "../Videos";
import Videocard from "../Videocard";
import { videoInit } from "../Videos";
import axios from "axios";
import { API_URL } from "../../constants";

interface Props {
  videoId: number,
}

export default function Morevideos(props: Props) {
  const [moreVideos, setMoreVideos] = React.useState<VideoType[]>(videoInit);

  React.useEffect(()=>{
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
      });
  }, []);

  const morevideos = moreVideos.map((video) => {
    return (
      <Videocard
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
