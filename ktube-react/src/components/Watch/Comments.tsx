import Commenting from "./Commenting";
import React from "react";
import axios from "axios";
import { API_URL } from "../../constants";
import { useViewerContext } from "../../providers/ViewerProvider";
import { ChannelType } from "../Watchpage";
import Commentitem from "./Commentitem";
import CommentReplyItem from "./CommentReplyItem";
import { toggleItem } from "../../functions/fun";

const channelInit = {
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

const channelsInit = [channelInit];

export interface Comment {
  id: number;
  comment_text: string;
  channel: number;
  likes: number;
  dislikes: number;
  commented_on: string;
}

const commentInit = [
  {
    id: 0,
    comment_text: "",
    channel: 0,
    likes: 0,
    dislikes: 0,
    commented_on: "",
  },
];

const commentReplyInit = [
  {
    id: 0,
    reply: "",
    channel: 0,
    likes: 0,
    dislikes: 0,
    commented_on: "",
  },
];

export interface CommentReply {
  id: number;
  reply: string;
  channel: number;
  likes: number;
  dislikes: number;
  commented_on: string;
}

interface Props {
  videoId: number;
}

interface RepliesProps {
  comment: Comment;
  manyChannels: boolean;
  channels: ChannelType[];
}

const commentRepiesStyle = {
  display: "none",
};

const CommentWithReplies: React.FC<RepliesProps> = ({
  comment,
  manyChannels,
  channels,
}) => {
  const [commentReplies, setCommentReplies] =
    React.useState<Array<CommentReply>>(commentReplyInit);

  const repliesId = "repliesStyle" + comment.id;
  const toogleId = "replies-toggle" + comment.id;
  const unToogleId = "replies-untoggle" + comment.id;

  const toggleReplies = () => {
    toggleItem(repliesId, true);
    toggleItem(toogleId, false);
    toggleItem(unToogleId, true);
  };

  const untoggleReplies = () => {
    toggleItem(repliesId, false);
    toggleItem(toogleId, true);
    toggleItem(unToogleId, false);
  };

  React.useEffect(() => {
    if (comment.id !== 0) {
      axios({
        method: "get",
        url: API_URL + "getReplies/" + String(comment.id),
      })
        .then((res) => setCommentReplies(res.data))
        .catch((error) => {
          console.log(error);
        });
    }
  }, []);

  const showCommentReplies = commentReplies.map((commentReply) => {
    return (
      <CommentReplyItem
        key={commentReply.id}
        reply={commentReply}
        manyChannels={manyChannels}
        channels={channels}
      />
    );
  });

  if (commentReplies.length > 0) {
    return (
      <React.Fragment key={comment.id}>
        <Commentitem
          comment={comment}
          manyChannels={manyChannels}
          channels={channels}
        />
        <div className="row">
          <div className="col-lg-3">
            <a onClick={toggleReplies} id={"replies-toggle" + comment.id}>
              <small>Show Replies</small>
            </a>
            <a
              onClick={untoggleReplies}
              id={"replies-untoggle" + comment.id}
              style={commentRepiesStyle}
            >
              <small>Hide Replies</small>
            </a>
          </div>
        </div>
        <div
          className="col-lg-12"
          id={"repliesStyle" + comment.id}
          style={commentRepiesStyle}
        >
          {showCommentReplies}
        </div>
      </React.Fragment>
    );
  } else {
    return (
      <React.Fragment key={comment.id}>
        <Commentitem
          comment={comment}
          manyChannels={manyChannels}
          channels={channels}
        />
      </React.Fragment>
    );
  }
};

const Comments = (props: Props) => {
  const viewerProvided = useViewerContext();
  const [manyChannels, setManyChannels] = React.useState<boolean>(false);
  const [channels, setChannels] = React.useState<Array<ChannelType>>(channelsInit);
  const [comments, setComments] = React.useState<Array<Comment>>(commentInit);
  const myToken = useViewerContext().myToken;

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
  }, [props.videoId]);

  React.useEffect(() => {
    if (myToken && viewerProvided.viewer.id !== 0) {
      axios({
        method: "get",
        url: API_URL + "getChannels/" + String(viewerProvided.viewer.id),
        headers: {
          Authorization: `Token ${myToken}`,
        },
      })
        .then((res) => {
          const channelsData = res.data?.channels;
          setChannels(channelsData);
          if (channelsData?.length > 1) {
            setManyChannels(true);
          }
        })
        .catch((error) => {
          console.log(error);
        });
    }
  }, [viewerProvided.viewer.id]);

  const showComments = comments.map((comment) => (
    <CommentWithReplies
      key={comment.id}
      comment={comment}
      manyChannels={manyChannels}
      channels={channels}
    />
  ));

  return (
    <>
      <Commenting
        videoId={props.videoId}
        channels={channels}
        manyChannels={manyChannels}
      />
      <div className="row">
        <h4 className="col-lg-12 box-element" id="comment-heading">
          Comments
        </h4>
      </div>

      <div className="col-lg-12" id="comment-section">
        {showComments}
      </div>
    </>
  );
};

export default Comments;
