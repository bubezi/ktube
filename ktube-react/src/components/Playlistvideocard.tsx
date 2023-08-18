import axios from "axios";
import React from "react";
import { imageStyle, priceStyle, 
  // height180px 
} from "../assets/styles/WatchStyles";
import { API_URL, API_BASE_URL } from "../constants";
import Videooptions from "./Options/Videooptions";
import { ChannelDetailsState } from "./Videocard";
import { VideoType } from "./Videos";
import imagePlaceholder from "../assets/images/placeholder.png";

interface Props {
  video: VideoType;
}

const Playlistvideocard: React.FC<Props> = ({ video }) => {
  const channelDetailsState: ChannelDetailsState = {
    profile_picture: "",
    name: "",
  };
  const [channelDetails, setChannelDetails] =
    React.useState<ChannelDetailsState>(channelDetailsState);

  React.useEffect(() => {
    if (Number(video.channel) !== 0) {
      axios
        .get(API_URL + "dp/" + video.channel)
        .then((res) => setChannelDetails(res.data))
        .catch((error) => {
          console.log(error);
        });
    }
  }, [video.channel]);

  const pluralViews = video.views === 1 ? "view" : "views";

  const Price = () => {
      if (video.price>0) {
          return (<h6 style={priceStyle}>KShs. { video.price }</h6>);
      }else{
          return (<></>);
      }
  }

  const ChannelDP = () => {
    if (channelDetails.profile_picture === "") {
      return (
        <img
          src={imagePlaceholder}
          className="channel-icon"
          alt="Channel Profile picture"
          style={imageStyle}
        />
      );
    } else {
      return (
        <img
          src={channelDetails.profile_picture}
          className="channel-icon"
          alt="Channel Profile picture"
          style={imageStyle}
        />
      );
    }
  };

  return (
    <React.Fragment key={video.id}>
      <div
        className="col-lg-12"
        // style={height180px}
      >
        <div className="row">
          <div className="col-lg-4">
            <a href={"/watch/" + video.slug}>
              <img
                src={API_BASE_URL + video.thumbnail}
                alt="thumbnail"
                className="thumbnail"
              />
            </a>
          </div>
          <div className="col-lg-8">
            <div className="row">
              <h4>{video.title}</h4>
            </div>
            <div className="row">
              <a href={"/channel/" + video.channel}>
                <ChannelDP />
              </a>
              <a href={"/channel/" + video.channel}>
                <h6>{channelDetails.name}</h6>
              </a>
            </div>
            <div className="row">
              <div className="col-lg-2">
                <Price/>
              </div>
              <div className="col-lg-10"></div>
            </div>
            <div className="row">
              <div className="col-lg-10">
                <div className="row">
                  <h6 id="video-views">
                    {video.views} {pluralViews}
                  </h6>
                </div>
              </div>
              <div className="col-lg-2 col-12 text-right mt-2 mt-lg-0">
                <Videooptions videoId={video.id} />
              </div>
            </div>
          </div>
        </div>
      </div>
    </React.Fragment>
  );
};

export default Playlistvideocard;
