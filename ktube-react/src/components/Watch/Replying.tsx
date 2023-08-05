import React from "react";
import { commentButton } from "../../assets/styles/WatchStyles";
import { Channel } from "../Watchpage";
import axios from "axios";
import { API_URL } from "../../constants";
import { toggleItem } from "../../functions/fun";
import { useViewerContext } from "../../providers/ViewerProvider";

interface Props {
  commentId: number;
  channels: Channel[];
  manyChannels: Boolean;
}

const formStyle = {
  display: "none",
};

const marginLeft = {
  marginLeft: "30px",
};

const marginLeft2 = {
  marginLeft: "10px",
};

const Replying = (props: Props) => {
  const [replyText, setReplyText] = React.useState<string>("");
  const [channelId, setChannelId] = React.useState<number>(0);
  const myToken = useViewerContext().myToken;

  const toggleId = "reply-toggle" + props.commentId;
  const untoggleId = "reply-untoggle" + props.commentId;
  const toggleFormMany = () => {
    const formId = "reply-many-channels-form" + props.commentId;
    toggleItem(formId, true);
    toggleItem(toggleId, false);
    toggleItem(untoggleId, true);
  };

  const toggleForm = () => {
    const formId = "reply-form" + props.commentId;
    toggleItem(formId, true);
    toggleItem(toggleId, false);
    toggleItem(untoggleId, true);
  };

  const untoggleFormMany = () => {
    const formId = "reply-many-channels-form" + props.commentId;
    toggleItem(formId, false);
    toggleItem(toggleId, true);
    toggleItem(untoggleId, false);
  };

  const untoggleForm = () => {
    const formId = "reply-form" + props.commentId;
    toggleItem(formId, false);
    toggleItem(toggleId, true);
    toggleItem(untoggleId, false);
  };

  const handleReply = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    try {
      const formData = new FormData();
      formData.append("reply_text", replyText);
      formData.append("comment_id", props.commentId.toString());

      const response = await axios.post(API_URL + "reply", formData, {
        headers: {
          Authorization: `Token ${myToken}`,
          "Content-Type": "multipart/form-data",
        },
      });

      if (response.status === 201) {
        setReplyText("");
        alert("Reply Added");
      } else {
        // Handle error response
        console.error("Failed to submit reply");
        // Display error message to the user
      }
    } catch (error) {
      // Handle network error
      console.error("Network error:", error);
      // Display error message to the user
    }
  };

  const handleManyChannelsReply = async (
    e: React.FormEvent<HTMLFormElement>
  ) => {
    e.preventDefault();

    if (channelId !== 0) {
      try {
        const formData = new FormData();
        formData.append("reply_text", replyText);
        formData.append("comment_id", props.commentId.toString());
        formData.append("channel_id", channelId.toString());

        const response = await axios.post(
          API_URL + "replyManyChannels",
          formData,
          {
            headers: {
              Authorization: `Token ${myToken}`,
              "Content-Type": "multipart/form-data",
            },
          }
        );

        if (response.status === 201) {
          setReplyText("");
          alert("Reply Added");
        } else {
          // Handle error response
          console.error("Failed to submit reply");
          // Display error message to the user
        }
      } catch (error) {
        // Handle network error
        console.error("Network error:", error);
        // Display error message to the user
      }
    }
  };

  if (myToken) {
    if (!props.manyChannels) {
      return (
        <>
          <a id={"reply-toggle" + props.commentId} onClick={toggleForm}>
            <small>Reply</small>
          </a>
          <a
            id={"reply-untoggle" + props.commentId}
            onClick={untoggleForm}
            style={formStyle}
          >
            <small>Hide</small>
          </a>
          <form
            style={formStyle}
            id={"reply-form" + props.commentId}
            onSubmit={handleReply}
          >
            <fieldset style={marginLeft}>
              <div className="row">
                <textarea
                  rows={2}
                  cols={75}
                  maxLength={350}
                  id="reply-text"
                  name="reply_text"
                  value={replyText}
                  onChange={(e) => setReplyText(e.target.value)}
                ></textarea>
              </div>
              <div className="row" style={commentButton}>
                <button
                  className="btn btn-success"
                  type="submit"
                  disabled={!replyText}
                >
                  Reply
                </button>
              </div>
            </fieldset>
          </form>
        </>
      );
    } else {
      const options = props.channels.map((channel) => {
        const value = `${channel.id}`;
        const name = `${channel.name}`;
        return (
          <option key={channel.id} value={value}>
            {name}
          </option>
        );
      });
      return (
        <>
          <a id={"reply-toggle" + props.commentId} onClick={toggleFormMany}>
            <small>Reply</small>
          </a>
          <a
            id={"reply-untoggle" + props.commentId}
            onClick={untoggleFormMany}
            style={formStyle}
          >
            <small>Hide</small>
          </a>
          <form
            style={formStyle}
            id={"reply-many-channels-form" + props.commentId}
            onSubmit={handleManyChannelsReply}
          >
            <fieldset style={marginLeft}>
              <div className="row">
                <textarea
                  rows={2}
                  cols={75}
                  maxLength={350}
                  id="reply-text"
                  name="reply_text"
                  value={replyText}
                  onChange={(e) => setReplyText(e.target.value)}
                ></textarea>
              </div>
              <div className="row">
                <div className="col-lg-12">
                  <div className="row">
                    <label htmlFor="channel-id">Select channel</label>
                  </div>
                  <div className="row">
                    <select
                      name="channel_id"
                      id="channel-id"
                      onChange={(e) => setChannelId(Number(e.target.value))}
                    >
                      <option key="select_channel" value={0}>
                        Select Channel
                      </option>
                      {options}
                    </select>
                  </div>
                </div>
              </div>
              <div className="row" style={commentButton}>
                <button
                  className="btn btn-success"
                  type="submit"
                  disabled={!replyText || channelId === 0}
                >
                  Reply
                </button>
              </div>
            </fieldset>
          </form>
          <br />
        </>
      );
    }
  } else {
    return (
      <a href="/auth/login" target="_blank">
        <h6 className="row" style={marginLeft2}>
          <small>
            <small>Login to reply</small>
          </small>
        </h6>
      </a>
    );
  }
};

export default Replying;
