import axios from "axios";
import React from "react";
import { useParams } from "react-router-dom";
import { API_URL } from "../constants";
import Videoview from "./Watch/Videoview";
import Watchpagecontainer from "./Watch/Watchpagecontainer";
import Morevideos from "./Watch/Morevideos";
import {
  mainColStyle,
  mainRowStyle,
  paddingLeft10,
  paddingLeft45,
} from "../assets/styles/WatchStyles";
import { PlaylistChannel } from "./Channel";
import { playlistInit } from "./Playlist";
import Moreplaylistvideos from "./Watch/Moreplaylistvideos";

export interface Video {
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
  website_official: "",
  channel_active: false,
  about: "",
};

export const videoInit = {
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

const Watchplaylist = () => {
  const { playlistId, positionN } = useParams();
  const [channel, setChannel] = React.useState<ChannelType>(channelInit);
  const [video, setVideo] = React.useState<Video>(videoInit);
  const [playlist, setPlaylist] = React.useState<PlaylistChannel>(playlistInit);
  const [position, setPosition] = React.useState<number>(-1);

  React.useEffect(() => {
    if (Number(positionN) !== 0) {
      setPosition(Number(positionN) - 1);
    }
  }, [positionN]);

  React.useEffect(() => {
    axios({
      method: "get",
      url: API_URL + "playlistAPI/" + playlistId,
      // headers: {
      //   Authorization: `Token ${myToken}`,
      // },
    })
      .then((res) => {
        setPlaylist(res.data);
      })
      .catch((error) => {
        console.log(error);
      });
  }, [playlistId]);

  React.useEffect(() => {
    if (
      playlist.videos[position] !== 0 &&
      playlist.id !== 0 &&
      position !== -1
    ) {
      axios({
        method: "get",
        url: API_URL + "watch/p/" + String(playlist.videos[Number(position)]),
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
    }
  }, [playlist, position]);

  React.useEffect(() => {
    if (playlist.name !== "") {
      document.title = video.title + " | " + playlist.name;
    }
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
  }, [video, playlist]);

  const pluralVideos = playlist.videos.length === 1 ? "video" : "videos";

  const PlaylistNav = () => {
    const Nav = () => {
      if (playlist.videos.length === 1) {
        return (
          <div>
            <button disabled={true} className="btn btn-outline-secondary">
              Prev
            </button>
            <button disabled={true} className="btn btn-outline-secondary">
              Next
            </button>
          </div>
        );
      } else if (Number(positionN) === 1 && playlist.videos.length > 1) {
        return (
          <div>
            <button disabled={true} className="btn btn-outline-secondary">
              Prev
            </button>
            <a
              href={
                "/watchplaylist/" + playlist.id + "/" + (Number(positionN) + 1)
              }
            >
              <button className="btn btn-outline-secondary">Next</button>
            </a>
          </div>
        );
      } else if (
        playlist.videos.length === Number(positionN) &&
        playlist.videos.length > 1
      ) {
        return (
          <div>
            <a
              href={
                "/watchplaylist/" + playlist.id + "/" + (Number(positionN) - 1)
              }
            >
              <button className="btn btn-outline-secondary">Previous</button>
            </a>
            <button disabled={true} className="btn btn-outline-secondary">
              Next
            </button>
          </div>
        );
      } else {
        return (
          <div>
            <a
              href={
                "/watchplaylist/" + playlist.id + "/" + (Number(positionN) - 1)
              }
            >
              <button className="btn btn-outline-secondary">Previous</button>
            </a>
            <a
              href={
                "/watchplaylist/" + playlist.id + "/" + (Number(positionN) + 1)
              }
            >
              <button className="btn btn-outline-secondary">Next</button>
            </a>
          </div>
        );
      }
    };
    return (
      <>
        <div className="col-lg-11 box-element">
          <div className="row" style={paddingLeft10}>
            <Nav />
            <h5 style={paddingLeft10}>
              (video {positionN} of {playlist.videos.length}{" "}{pluralVideos}) - {playlist.name}
            </h5>
          </div>
        </div>
      </>
    );
  };

  return (
    <>
      <div className="row" style={mainRowStyle}>
        <div className="col-lg-9" style={mainColStyle}>
          <Videoview video={video.video} />
          <div className="row" style={paddingLeft45}>
            <PlaylistNav />
          </div>
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
          <Moreplaylistvideos
            videoId={video.id}
            playlist={playlist}
            position={Number(positionN)}
          />
          <Morevideos videoId={video.id} />
        </div>
      </div>
    </>
  );
};

export default Watchplaylist;
