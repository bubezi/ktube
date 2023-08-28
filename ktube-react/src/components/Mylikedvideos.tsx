import { useViewerContext } from "../providers/ViewerProvider";
import Videocard from "./Videocard";
import axios from "axios";
import { API_BASE_URL, API_URL } from "../constants";
import React from "react";
import { VideoType } from "./Videos";

const Mylikedvideos = () => {
  const myToken = useViewerContext().myToken;
  const [myLikedVideos, setMyLikedVideos] = React.useState<VideoType[]>([]);

  if (myToken) {
    document.title = "My Liked Videos | KTUBE";

    React.useEffect(() => {
      axios({
        method: "get",
        url: API_URL + "myLikedVideosAPI",
        headers: {
          Authorization: `Token ${myToken}`,
        },
      })
        .then((res) => {
          if (Array.isArray(res.data.MyLikedVideos)) {
            setMyLikedVideos(res.data.MyLikedVideos);
          } else {
            setMyLikedVideos(Array(res.data.MyLikedVideos));
          }
        })
        .catch((error) => {
          console.log(error);
        });
    }, [myToken]);

    const MyLikedVideos = () => {
      const pluralMyLikedVideos = myLikedVideos.length === 1 ? "video" : "videos";

      const showMylikedVideos = myLikedVideos.map((likedVideo) => {
        return (
          <Videocard
            key={likedVideo.id}
            channelId={likedVideo.channel}
            colSize="4"
            price={likedVideo.price}
            slug={likedVideo.slug}
            thumbnail={API_BASE_URL + likedVideo.thumbnail}
            title={likedVideo.title}
            videoId={likedVideo.id}
            views={likedVideo.views}
          />
        );
      });

      return (
        <>
          <div className="row box-element">
            <div className="col-lg-12">
              <div className="row">
                <h3>
                  My Liked Videos - {myLikedVideos.length} {pluralMyLikedVideos}
                </h3>
              </div>
            </div>
          </div>
          <div className="row">{showMylikedVideos}</div>
        </>
      );
    };

    return (
      <>
        <div className="container">
          <MyLikedVideos />
        </div>
      </>
    );
  } else {
    location.assign("/auth/login");
  }
};

export default Mylikedvideos;
