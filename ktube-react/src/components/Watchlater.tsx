import axios from "axios";
import React from "react";
import { API_URL, API_BASE_URL } from "../constants";
import { useViewerContext } from "../providers/ViewerProvider";
import Videocard from "./Videocard";
import { VideoType } from "./Videos";

const Watchlater = () => {
  const myToken = useViewerContext().myToken;
  const [watchlaterVideos, setWatchlaterVideos] = React.useState<VideoType[]>(
    []
  );

  if (myToken) {
    React.useEffect(() => {
      axios({
        method: "get",
        url: API_URL + "watchlaterVideos",
        headers: {
          Authorization: `Token ${myToken}`,
        },
      })
        .then((res) => {
          if (Array.isArray(res.data.watchlater)) {
            setWatchlaterVideos(res.data.watchlater);
          } else {
            setWatchlaterVideos(Array(res.data.watchlater));
          }
        })
        .catch((error) => {
          console.log(error);
        });
    }, [myToken]);

    document.title = "My Watchlater | KTUBE";

    const Mywatchlater = () => {
      const pluralVideos = watchlaterVideos.length === 1 ? "Video" : "Videos";

      const showWatchltervideos = watchlaterVideos.map((video) => {
        return (
          <>
            <Videocard
              key={video.id}
              channelId={video.channel}
              colSize="4"
              price={video.price}
              slug={video.slug}
              thumbnail={API_BASE_URL + video.thumbnail}
              title={video.title}
              videoId={video.id}
              views={video.views}
            />
          </>
        );
      });

      return (
        <>
          <div className="row box-element">
            <div className="col-lg-12">
              <div className="row">
                <h3>
                  My Watchlater - {watchlaterVideos.length} {pluralVideos}
                </h3>
              </div>
            </div>
          </div>
          <div className="row">{showWatchltervideos}</div>
        </>
      );
    };

    return (
      <>
        <div className="container">
          <Mywatchlater />
        </div>
      </>
    );
  } else {
    location.assign("/auth/login");
  }
};

export default Watchlater;
