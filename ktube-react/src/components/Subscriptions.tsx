import React from "react";
import { useViewerContext } from "../providers/ViewerProvider";
import SubedChannelsCard from "./SubedChannelsCard";
import axios from "axios";
import { API_BASE_URL, API_URL } from "../constants";
import Videocard from "./Videocard";
import { Video } from "./Watchpage";

interface Channel {
  id: number;
  name: string;
  about: string;
}

const Subscriptions = () => {
  const myToken = useViewerContext().myToken;
  const [subscribedChannels, setSubscribedChannels] = React.useState<
    Array<Channel>
  >([]);
  const [subscribedChannelsVideos, setSubscribedChannelsVideos] = React.useState<
    Array<Video>
  >([]);

  if (myToken) {
    document.title = "My Subscriptions | KTUBE";

    React.useEffect(() => {
        axios({
          method: "get",
          url: API_URL + "subedChannels",
          headers: {
            Authorization: `Token ${myToken}`,
          },
        })
          .then((res) => {
            if (Array.isArray(res.data)) {
              setSubscribedChannels(res.data);
            } else {
              setSubscribedChannels(Array(res.data));
            }
          })
          .catch((error) => {
            console.log(error);
          });

          axios({
            method: "get",
            url: API_URL + "subedChannelsVideos",
            headers: {
              Authorization: `Token ${myToken}`,
            },
          })
            .then((res) => {
              if (Array.isArray(res.data)) {
                setSubscribedChannelsVideos(res.data);
              } else {
                setSubscribedChannelsVideos(Array(res.data));
              }
            })
            .catch((error) => {
              console.log(error);
            });
    }, [myToken]);

    const SubscribedChannels = () => {
      const pluralChannels =
        subscribedChannels.length === 1 ? "Channel" : "Channels";

      const showChannels = subscribedChannels.map((channel) => {
        return (
          <SubedChannelsCard
            key={channel.id}
            name={channel.name}
            description={channel.about}
          />
        );
      });

      return (
        <>
          <div className="row box-element">
            <div className="col-lg-12">
              <div className="row">
                <h3>
                  Subscriptions - {subscribedChannels.length} {pluralChannels}
                </h3>
              </div>
            </div>
          </div>
          <div className="row">{showChannels}</div>
        </>
      );
    };

    const SubscribedChannelsVideos = () => {
      const pluralVideos =
        subscribedChannelsVideos.length === 1 ? "Video" : "Videos";

      const showVideos = subscribedChannelsVideos.map((video) => {
        return (
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
        );
      });

      return (
        <>
          <div className="row box-element">
            <div className="col-lg-12">
              <div className="row">
                <h3>
                  Videos - {subscribedChannelsVideos.length}{" "}
                  {pluralVideos}
                </h3>
              </div>
            </div>
          </div>
          <div className="row">{showVideos}</div>
        </>
      );
    };
    return (
      <>
        <div className="container">
          <SubscribedChannels />
          <SubscribedChannelsVideos />
        </div>
      </>
    );
  } else {
    location.assign("/auth/login");
  }
};

export default Subscriptions;
