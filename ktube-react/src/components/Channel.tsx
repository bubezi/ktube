import imagePlaceholder from "../assets/images/placeholder.png";
import React from "react";
import { useParams } from "react-router-dom";
import { channelInit } from "./Watchpage";
import { ChannelType } from "./Watchpage";
import { Video } from "./Watchpage";
import { videoInit } from "./Watchpage";
import axios from "axios";
import { API_BASE_URL, API_URL } from "../constants";
import Footer from "./Footer";
import {
  channelDpStyle,
  marginLeft40,
  marginLeft60,
  marginTopN22,
  paddingLeft45,
  paddingTop35,
  paddingTop3,
} from "../assets/styles/WatchStyles";
import { useViewerContext } from "../providers/ViewerProvider";
import Subscribe from "./Subscribe";
import Videocard from "./Videocard";
import { channelVideosStyle } from "../assets/styles/Styles";
import Playlistcard from "./Playlistcard";

const videosInit = [videoInit];

export interface PlaylistChannel {
  id: number;
  name: string;
  views: number;
  public: boolean;
  created_on: string;
  channel: string;
  videos: number[];
}

const Channel = () => {
  const { channelId } = useParams();
  const myToken = useViewerContext().myToken;
  const viewerId = useViewerContext().viewer.id;
  const [channel, setChannel] = React.useState<ChannelType>(channelInit);
  const [videos, setVideos] = React.useState<Array<Video>>(videosInit);
  const [unlistedVideos, setUnlistedVideos] =
    React.useState<Array<Video>>(videosInit);
  const [privateVideos, setPrivateVideos] =
    React.useState<Array<Video>>(videosInit);
  const [playlists, setPlaylists] = React.useState<Array<PlaylistChannel>>([]);
  const [subscriberCount, setSubscriberCount] = React.useState<number>(0);
  const [owner, setOwner] = React.useState<boolean>(false);

  React.useEffect(() => {
    if (Number(channelId) !== 0) {
      axios({
        method: "get",
        url: API_URL + "channel/" + channelId,
      })
        .then((res) => {
          setChannel(res.data);
        })
        .catch((error) => {
          console.log(error);
        });

      axios({
        method: "get",
        url: API_URL + "channelVideos/" + channelId,
      })
        .then((res) => {
          setVideos(res.data);
        })
        .catch((error) => {
          console.log(error);
        });

      axios({
        method: "get",
        url: API_URL + "channelUnlistedVideos/" + channelId,
      })
        .then((res) => {
          setUnlistedVideos(res.data);
        })
        .catch((error) => {
          console.log(error);
        });

      axios({
        method: "get",
        url: API_URL + "channelPrivateVideos/" + channelId,
      })
        .then((res) => {
          setPrivateVideos(res.data);
        })
        .catch((error) => {
          console.log(error);
        });

      axios({
        method: "get",
        url: API_URL + "channelPlaylists/" + channelId,
      })
        .then((res) => {
          setPlaylists(res.data);
        })
        .catch((error) => {
          console.log(error);
        });
    }
  }, [channelId]);

  React.useEffect(() => {
    setSubscriberCount(channel.subscribers.length);

    if (channel.name !== "") {
      document.title = channel.name + " | KTUBE";
    }

    if (myToken !== null && channel.id !== 0) {
      axios({
        method: "get",
        url: API_URL + "isowner/" + String(channel.id),
        headers: {
          Authorization: `Token ${myToken}`,
        },
      })
        .then((res) => {
          const channelOwner = res.data?.is_owner;
          setOwner(channelOwner);
        })
        .catch((error) => {
          console.log(error);
        });
    }
  }, [channel]);

  const Profilepicture = () => {
    if (channel.profile_picture !== "") {
      return (
        <img
          src={API_BASE_URL + channel.profile_picture}
          className="channel-icon"
          alt="Channel Profile picture"
          style={channelDpStyle}
        />
      );
    } else {
      return (
        <img
          src={imagePlaceholder}
          className="channel-icon"
          alt="Channel Profile picture placeholder"
          style={channelDpStyle}
        />
      );
    }
  };

  const Subscribercount = () => {
    if (subscriberCount === 1) {
      return (
        <h5 id="subscriber-count" style={paddingLeft45}>
          {subscriberCount} Subscriber
        </h5>
      );
    } else {
      return (
        <h5 id="subscriber-count" style={paddingLeft45}>
          {subscriberCount} Subscribers
        </h5>
      );
    }
  };

  const Actions = () => {
    if (owner) {
      return (
        <>
          <a href={"/editChannel/" + channel.id}>
            <button
              className="btn btn-outline-secondary add-btn update-cart"
              style={marginLeft40}
            >
              Edit Channel
            </button>
          </a>
          <a href={"/upload/" + channel.id}>
            <button className="btn btn-success" style={marginLeft40}>
              Upload
            </button>
          </a>
          <a href="/live">
            <button className="btn btn-success" style={marginLeft40}>
              Go live
            </button>
          </a>
        </>
      );
    } else {
      return (
        <>
          <Subscribe
            subscribers={channel.subscribers}
            channelId={channel.id}
            channelUserId={channel.user}
            setSubscriberCount={setSubscriberCount}
            subscriberCount={subscriberCount}
            marginLeft={marginLeft60}
          />
        </>
      );
    }
  };

  const Videocount = () => {
    if (videos.length === 1) {
      return <h4 style={channelVideosStyle}>{videos.length} Video</h4>;
    } else {
      return <h4 style={channelVideosStyle}>{videos.length} Videos</h4>;
    }
  };

  const CreatePlaylistButton = () => {
    return (
      <>
        <a href={"/createPlaylist/" + viewerId}>
          <button className="btn btn-success" style={marginLeft40}>
            Create Playlist
          </button>
        </a>
      </>
    );
  };

  const PrivateSection = () => {
    const UnlistedVideos = () => {
      const showUnlistedVideos = unlistedVideos.map((unlistedVideo)=> {
        const thumbnailURL = API_BASE_URL + `${unlistedVideo.thumbnail}`;
        return (
          <Videocard
            channelId={unlistedVideo.channel}
            colSize="4"
            price={unlistedVideo.price}
            slug={unlistedVideo.slug}
            thumbnail={thumbnailURL}
            title={unlistedVideo.title}
            videoId={unlistedVideo.id}
            views={unlistedVideo.views}
            key={unlistedVideo.id}
          />
        );

      });
      return (
        <>
          <div className="row box-element">
            <h2>Unlisted videos</h2>
          </div>
          <div className="row">{showUnlistedVideos}</div>
        </>
      );
    };

    const PrivateVideos = () => {
      const showPrivateVideos = privateVideos.map((privateVideo)=> {
        const thumbnailURL = API_BASE_URL + `${privateVideo.thumbnail}`;
        return (
          <Videocard
            channelId={privateVideo.channel}
            colSize="4"
            price={privateVideo.price}
            slug={privateVideo.slug}
            thumbnail={thumbnailURL}
            title={privateVideo.title}
            videoId={privateVideo.id}
            views={privateVideo.views}
            key={privateVideo.id}
          />
        );

      });
      return (
        <>
          <div className="row box-element">
            <h2>Private videos</h2>
          </div>
          <div className="row">{showPrivateVideos}</div>
        </>
      );
    };
    if (owner) {
      return (
        <>
          <UnlistedVideos />
          <PrivateVideos />
        </>
      );
    } else {
      return <></>;
    }
  };
  const show_videos = videos.map((video) => {
    const thumbnailURL = API_BASE_URL + `${video.thumbnail}`;
    return (
      <Videocard
        channelId={video.channel}
        colSize="4"
        price={video.price}
        slug={video.slug}
        thumbnail={thumbnailURL}
        title={video.title}
        videoId={video.id}
        views={video.views}
        key={video.id}
      />
    );
  });

  const show_playlists = playlists.map((playlist) => {
    return <Playlistcard key={playlist.id} playlist={playlist} />;
  });

  if (channel.channel_active) {
    return (
      <>
        <div className="container" style={paddingTop35}>
          <div className="row box-element" style={marginTopN22}>
            <div className="col-lg-12">
              <div className="row">
                <Profilepicture />
                <h3>{channel.name}</h3>
              </div>
              <div className="row">
                <Subscribercount />
              </div>
              <div className="row">
                <Actions />
              </div>
            </div>
          </div>
          <div className="row box-element">
            <Videocount />
          </div>
          <div className="row">{show_videos}</div>
          <br />
          <div className="row box-element">
            <h3>Playlists</h3>
            <div className="row">
              <CreatePlaylistButton />
            </div>
          </div>
          <div className="row">{show_playlists}</div>
          <hr style={paddingTop3} />
          <PrivateSection />
        </div>
        <Footer />
      </>
    );
  } else {
    return (
      <>
        <div className="container" style={paddingTop35}>
          <h1>Channel Not Active</h1>
        </div>
      </>
    );
  }
};

export default Channel;
