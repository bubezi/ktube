import axios from "axios";
import React from "react";
import { paddingLeft10 } from "../assets/styles/WatchStyles";
import { API_URL } from "../constants";
import { PlaylistChannel } from "./Channel";
import { ChannelDetailsState } from "./Videocard";
import imagePlaceholder from "../assets/images/placeholder.png";
import Playlistoptions from "./Options/Playlistoptions";

interface Props {
  playlist: PlaylistChannel;
  colSize: string;
}

const Playlistcard = (props: Props) => {
  const channelDetailsState: ChannelDetailsState = {
    profile_picture: "",
    name: "",
  };
  const [channelDetails, setChannelDetails] =
    React.useState<ChannelDetailsState>(channelDetailsState);

  React.useEffect(() => {
    if (Number(props.playlist.channel) !== 0) {
      axios
        .get(API_URL + "dp/" + props.playlist.channel)
        .then((res) => setChannelDetails(res.data))
        .catch((error) => {
          console.log(error);
        });
    }
  }, [props.playlist.channel]);

  const channelDp = `${channelDetails.profile_picture}`;
  const videoChannelName = `${channelDetails.name}`;

  const imageStyle = {
    width: "20px",
    height: "20px",
  };

  const pluralViews = props.playlist.views === 1 ? "view" : "views";
  const pluralVideos = props.playlist.videos.length === 1 ? "Video" : "Videos";

  const ChannelDP = () => {
    if (channelDp === "") {
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
          src={channelDp}
          className="channel-icon"
          alt="Channel Profile picture"
          style={imageStyle}
        />
      );
    }
  };

  return (
    <>
      <div className={"col-lg-"+props.colSize +" "+"box-element"}>
        <div style={paddingLeft10}>
          <div className="row">
            <div className="col-lg-12">
              <div className="row">
                <a href={"/playlist/" + props.playlist.id}>
                  <h4>
                    {props.playlist.name} -{" "}
                    <small>
                      {props.playlist.videos.length} {pluralVideos}
                    </small>
                  </h4>
                </a>
              </div>
            </div>
          </div>
          <div className="row">
            <div className="col-lg-12">
              <div className="row">
                <a href={"/channel/" + props.playlist.channel}>
                  <ChannelDP />
                </a>
                <a href={"/channel/" + props.playlist.channel}>
                  <h6>{videoChannelName}</h6>
                </a>
              </div>
            </div>
          </div>
          <div className="row">
            <div className="col-lg-10">
                <div className="row">
                    {props.playlist.views} {pluralViews}
                </div>
            </div>
            <div className="col-lg-2  col-12 text-right mt-2 mt-lg-0"><Playlistoptions playlistId={props.playlist.id}/></div>
          </div>
        </div>
      </div>
    </>
  );
};

export default Playlistcard;
