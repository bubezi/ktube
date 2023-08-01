import Commenting from "./Commenting";
import React from "react";
import axios from "axios";
import { API_URL } from "../../constants";
import { useViewerContext } from "../../providers/ViewerProvider";
import { Channel } from "../Watchpage";
import Commentitem from "./Commentitem";
import { commentHeading } from "../../assets/styles/WatchStyles";
// import { channelInit } from "../Watchpage";

const channelInit = { id:0, name: "", profile_picture: "", subscriber_count: 0, private: true, unlisted:true, subscribers:[0], userId:0};

const channelsInit = [channelInit];


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

const Comments = (props: Props) => {
  const viewerProvided = useViewerContext();
  const [ owner, setOwner ] = React.useState<boolean>(false);
  const [ manyChannels, setManyChannels ] = React.useState<boolean>(false);
  const [ channels, setChannels ] = React.useState<Array<Channel>>(channelsInit);
  const [ comments, setComments ] = React.useState<Array<Comment>>(commentInit);
  const [ myToken ] = React.useState(() => {
    const savedToken = localStorage.getItem("token");
    return savedToken ?? null;
  });

  React.useEffect(() => {
    if (props.videoId !== 0) {
      axios({
        method: "get",
        url: API_URL + "getComments/" + String(props.videoId),
        // headers: {
        //   Authorization: `Token ${myToken}`,
        // },
      })
        .then((res) => setComments(res.data))
        .catch((error) => {
          console.log(error);
        });
    }

    if (myToken && viewerProvided.viewer.id !== 0){
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
    }

  }, []);

  React.useEffect(() => {
    if (channels[0].id !== 0){
      axios({
        method: "get",
        url: API_URL + "isowner/" + String(channels[0].id),
        headers: {
          Authorization: `Token ${myToken}`,
        },
      })
        .then((res) => setOwner(res.data.is_owner))
        .catch((error) => {
          console.log(error);
        });    
    }
  }, [channels]);

  const showComments = comments.map((comment) => {
    const [ commentReplies, setCommentReplies ] = React.useState<Array<Comment>>(commentInit);

    React.useEffect(() => {
      if (comment.id !== 0){
        axios({
          method: "get",
          url: API_URL + "getReplies/" + String(comment.id),
          // headers: {
          //   Authorization: `Token ${myToken}`,
          // },
        })
          .then((res) => setCommentReplies(res.data))
          .catch((error) => {
            console.log(error);
          });
      }
    }, []);

    const showCommentReplies = commentReplies.map((commentReply)=>{
      return (
        <Commentitem 
          key={commentReply.id}
          comment={commentReply}
          owner={owner}
          manyChannels={manyChannels}
          channels={channels}
        />
      );
    })

    return (
      <React.Fragment key={comment.id}>
        <Commentitem
          comment={comment}
          owner={owner}
          manyChannels={manyChannels}
          channels={channels}
        />
        {showCommentReplies}
      </React.Fragment>
    );
  });

  return (
    <>
      <Commenting videoId={props.videoId}/>
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

export default Comments;
