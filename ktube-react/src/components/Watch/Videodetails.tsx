import imagePlaceholder from "../../assets/images/placeholder.png";
import Subscribe from "../Subscribe";
import Viewsandoptions from "./Viewsandoptions";
import Likeanddislike from "./Likeanddislike";
import Description from "./Description";
import {
  channelStyle,
  dpStyle,
  publicityStyle,
  titleStyle,
} from "../../assets/styles/WatchStyles";
import { API_BASE_URL, API_URL } from "../../constants";
import React from "react";
import { useViewerContext } from "../../providers/ViewerProvider";
import axios from "axios";

interface Prop {
  title: string;
  channel: string;
  subscriber_count: number;
  private: boolean;
  unlisted: boolean;
  profile_picture: string;
  channelId: number;
  subscribers: number[];
  channelUserId: number;
  videoId: number;
  views: number;
  likes: number;
  dislikes: number;
  description: string;
  upload_time: string;
}

const Videodetails = (props: Prop) => {
  const [subscriberCount, setSubscriberCount] = React.useState<number>(
    props.subscriber_count
  );
  
  const myToken = useViewerContext().myToken;
  const viewerId = useViewerContext().viewer.id;

  React.useEffect(() => {
    setSubscriberCount(props.subscriber_count);
  }, [props.subscriber_count]);

  React.useEffect(()=>{
    setTimeout(async ()=>{

      const data = {
        video_id: props.videoId,
        viewer_id: viewerId,
      };
    
      const config = {
        headers: {
          "Content-Type": "application/json",
          Authorization: `Token ${myToken}`,
        },
      };
    
      if(props.videoId !== 0){
        await axios
          .post(API_URL + "addView", data, config)
          .then((response) => {
            console.log(response.data);
          })
          .catch((error) => {
            if (error.response) {
              // The request was made and the server responded with a status code
              // that falls out of the range of 2xx
              console.log(error.response.data);
              console.log(error.response.status);
              console.log(error.response.headers);
            } else if (error.request) {
              // The request was made but no response was received
              console.log(error.request);
            } else {
              // Something happened in setting up the request that triggered an Error
              console.log("Error", error.message);
            }
            console.log(error.config);
          });
      }
    }, 5000);
  },[props.videoId])

  const PrivateOrUnlisted = () => {
    if (props.private) {
      return <h6 style={publicityStyle}>(private)</h6>;
    } else {
      if (props.unlisted) {
        return <h6 style={publicityStyle}>(unlisted)</h6>;
      }
    }
  };

  const Profilepicture = () => {
    if (props.profile_picture !== "") {
      return (
        <img
          src={API_BASE_URL + props.profile_picture}
          className="channel-icon"
          alt="Channel Profile picture"
          style={dpStyle}
        />
      );
    } else {
      return (
        <img
          src={imagePlaceholder}
          className="channel-icon"
          alt="Channel Profile picture placeholder"
          style={dpStyle}
        />
      );
    }
  };

  const Subscribercount = () => {
    if (subscriberCount === 1) {
      return (
        <h5 id="subscriber-count" style={publicityStyle}>
          {subscriberCount} Subscriber
        </h5>
      );
    } else {
      return (
        <h5 id="subscriber-count" style={publicityStyle}>
          {subscriberCount} Subscribers
        </h5>
      );
    }
  };

  return (
    <>
      <div className="row box-element">
        <div className="col-lg-12">
          <div className="row">
            <div className="col-lg-12">
              <div className="row">
                <h6 style={titleStyle}>
                  <strong>{props.title}</strong>
                </h6>
                <PrivateOrUnlisted />
              </div>
              <div className="row">
                <Profilepicture />
                <a href={"/channel/" + String(props.channelId)}>
                  <h6 style={channelStyle}>
                    <strong>{props.channel}</strong>
                  </h6>
                </a>
                <h5 style={publicityStyle}>-</h5>
                <Subscribercount />
              </div>
            </div>
          </div>
          <Subscribe
            subscribers={props.subscribers}
            channelId={props.channelId}
            channelUserId={props.channelUserId}
            setSubscriberCount={setSubscriberCount}
            subscriberCount={subscriberCount}
          />
          <Viewsandoptions videoId={props.videoId} views={props.views} />
          <Likeanddislike
            videoId={props.videoId}
            likes={props.likes}
            dislikes={props.dislikes}
          />
          <Description
            description={props.description}
            upload_time={props.upload_time}
          />
          <br />
        </div>
      </div>
    </>
  );
};

export default Videodetails;
