import Commenting from "./Commenting";
import React from "react";
import axios from "axios";
import { API_URL } from "../../constants";
import { useViewerContext } from "../../providers/ViewerProvider";
import { Channel } from "../Watchpage";
import { channelInit } from "../Watchpage";
import Commentsection from "./Commentsection";

const channelsInit = [channelInit];

const viewerProvided = useViewerContext();

interface Props {
  videoId: number;
}

export interface Comment {
  id: number;
  comment_text: string;
  channel_dp: string;
  channel: string;
  likes: number;
  dislikes: number;
  commented_on: string;
}

const commentInit = [
  {
    id: 0,
    comment_text: "",
    channel_dp: "",
    channel: "",
    likes: 0,
    dislikes: 0,
    commented_on: "",
  },
];

export default function Comments(props: Props) {
  const [manyChannels, setManyChannels] = React.useState<boolean>(false);
  const [channels, setChannels] = React.useState<Array<Channel>>(channelsInit);
  const [comments, setComments] = React.useState<Array<Comment>>(commentInit);
  const [myToken] = React.useState(() => {
    const savedToken = localStorage.getItem("token");
    return savedToken ?? null;
  });

  React.useEffect(() => {
    axios({
      method: "get",
      url: API_URL + "getComments/" + String(props.videoId),
      headers: {
        Authorization: `Token ${myToken}`,
      },
    })
      .then((res) => setComments(res.data.comments))
      .catch((error) => {
        console.log(error);
      });

    axios({
      method: "get",
      url: API_URL + "getChannels/" + String(viewerProvided.viewer.id),
      headers: {
        Authorization: `Token ${myToken}`,
      },
    })
      .then((res) => {
        setChannels(res.data.channels);
        if (channels.length > 1) {
          setManyChannels(true);
        }
      })
      .catch((error) => {
        console.log(error);
      });
  }, []);

  const showComments = comments.map((comment) => {
    return (
      <>
        <Commentsection
          comment={comment}
          manyChannels={manyChannels}
          channels={channels}
        />
      </>
    );
  });

  return (
    <>
      <Commenting />
      <div className="row">
        <h4 className="col-lg-12 box-element" style={commentHeading}>
          Comments
        </h4>
      </div>

      <div className="col-lg-12" id="comment-section">
        {showComments}
      </div>
    </>
  );
}
