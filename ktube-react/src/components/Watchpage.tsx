import axios from "axios";
import React from "react";
import { useParams } from "react-router-dom";
import { API_URL } from "../constants";
import Videoview from "./Watch/Videoview";
import Watchpagecontainer from "./Watch/Watchpagecontainer";
import Morevideos from "./Watch/Morevideos";
import { mainColStyle, mainRowStyle } from "../assets/styles/WatchStyles";

interface Video {
  id: number;
  title: string;
  video: string;
  thumbnail: string;
  description: string;
  upload_time: string;
  channel: number;
  private: boolean;
  unlisted: boolean;
  likes: number;
  dislikes: number;
  views: number;
  slug: string;
  path: string;
  price: number;
}


export interface ChannelType {
  id: number;
  name: string;
  profile_picture: string;
  user: number;
  private: boolean;
  unlisted: boolean;
  subscribers: number[];
  website_official: string;
  channel_active: boolean;
  about: string;
}

export const channelInit = {
  id: 0,
  name: "",
  profile_picture: "",
  user: 0,
  private: true,
  unlisted: true,
  subscribers: [0],
  website_official: '',
  channel_active: false,
  about: '',
};

const Watchpage = () => {
  const videoInit = {
    id: 0,
    title: "",
    video: "",
    thumbnail: "",
    description: "",
    upload_time: "",
    channel: 0,
    private: true,
    unlisted: true,
    likes: 0,
    dislikes: 0,
    views: 0,
    slug: "",
    path: "",
    price: 0,
  };

  const [channel, setChannel] = React.useState<ChannelType>(channelInit);
  const [video, setVideo] = React.useState<Video>(videoInit);
  const { slug } = useParams();

  React.useEffect(() => {
    // Fetch data from Django backend using `slug`
    axios({
      method: "get",
      url: API_URL + "watch/v/" + slug,
      // headers: {
      //   Authorization: `Token ${myToken}`,
      // },
    })
      .then((res) => {
        setVideo(res.data);
      })
      .catch((error) => {
        console.log(error);
      });
  }, [slug]);

  React.useEffect(() => {
    document.title = video.title + " | KTUBE";
    if (video.channel !== 0 && channel.id === 0) {
      axios({
        method: "get",
        url: API_URL + "channel/" + video.channel,
        // headers: {
        //   Authorization: `Token ${myToken}`,
        // },
      })
        .then((res) => {
          setChannel(res.data);
        })
        .catch((error) => {
          console.log(error);
        });
    }
  }, [video, channel]);

  return (
    <>
      <div className="row" style={mainRowStyle}>
        <div className="col-lg-9" style={mainColStyle}>
          <Videoview video={video.video} />

          <Watchpagecontainer
            title={video.title}
            channel={channel.name}
            subscriber_count={channel.subscribers.length}
            private={channel.private}
            unlisted={channel.unlisted}
            profile_picture={channel.profile_picture}
            channelId={channel.id}
            subscribers={channel.subscribers}
            channelUserId={channel.user}
            videoId={video.id}
            views={video.views}
            likes={video.likes}
            dislikes={video.dislikes}
            description={video.description}
            upload_time={video.upload_time}
          />
        </div>
        <div className="col-lg-3">
          <Morevideos videoId={video.id} />
        </div>
      </div>
    </>
  );
};

export default Watchpage;
