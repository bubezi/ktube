import axios from "axios";
import React from "react";
import { API_BASE_URL, API_URL } from "../constants";
import Videocard from "./Videocard";
import { VideoType } from "./Videos";
import { useViewerContext } from "../providers/ViewerProvider";

const Myhistory = () => {
  const myToken = useViewerContext().myToken;
  const [myHistory, setMyHistory] = React.useState<VideoType[]>([]);

  if (myToken) {
    document.title = "My History | KTUBE";

    React.useEffect(() => {
      axios({
        method: "get",
        url: API_URL + "myHistoryAPI",
        headers: {
          Authorization: `Token ${myToken}`,
        },
      })
        .then((res) => {
          if (Array.isArray(res.data.MyHistory)) {
            setMyHistory(res.data.MyHistory);
          } else {
            setMyHistory(Array(res.data.MyHistory));
          }
        })
        .catch((error) => {
          console.log(error);
        });
    }, [myToken]);

    const pluralMyHistory = myHistory.length === 1 ? "video" : "videos";

    const showMyHistory = myHistory.map((video, index) => {
      return (
        <Videocard
          key={index}
          colSize="4"
          channelId={video.channel}
          price={video.price}
          slug={video.slug}
          thumbnail={API_BASE_URL + video.thumbnail}
          title={video.title}
          videoId={video.id}
          views={video.views}
        />
      );
    });

    return (
      <>
      <div className="container">
        <div className="row box-element">
          <div className="col-lg-12">
            <div className="row">
              <h3>
                My History - {myHistory.length} {pluralMyHistory}
              </h3>
            </div>
          </div>
        </div>
        <div className="row">{showMyHistory}</div>
      </div>
      </>
    );
  };
  
  }


export default Myhistory;
