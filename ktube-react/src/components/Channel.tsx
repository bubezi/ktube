import imagePlaceholder from "../assets/images/placeholder.png";
import React from "react";
import { useParams } from "react-router-dom";
import { channelInit } from "./Watchpage";
import { ChannelType } from "./Watchpage";
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
} from "../assets/styles/WatchStyles";
import { useViewerContext } from "../providers/ViewerProvider";
import Subscribe from "./Subscribe";

const Channel = () => {
  const { channelId } = useParams();
  const myToken = useViewerContext().myToken;
  const [channel, setChannel] = React.useState<ChannelType>(channelInit);
  const [subscriberCount, setSubscriberCount] = React.useState<number>(0);
  const [owner, setOwner] = React.useState<boolean>(false);

  React.useEffect(() => {
    if (Number(channelId) !== 0) {
      axios({
        method: "get",
        url: API_URL + "channel/" + channelId,
        // headers: {
        //   Authorization: `Token ${myToken}`,
        // },
      })
        .then((res) => {
          console.log("response data: ", res.data);
          setChannel(res.data);
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
