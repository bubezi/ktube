import React from "react";
import { commentButton } from "../../assets/styles/WatchStyles";
import { Channel } from "../Watchpage";
import axios from "axios";
import { API_URL } from "../../constants";

interface Props {
  videoId: number;
  channels: Channel[];
  manyChannels: Boolean;
}

const Commenting = (props: Props) => {
  const [commentText, setCommentText] = React.useState<string>("");
  const [channelId, setChannelId] = React.useState<number>(0);
  const [myToken] = React.useState(() => {
    const savedToken = localStorage.getItem("token");
    return savedToken ?? null;
  });

 
  const handleComment = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    try {
      const formData = new FormData();
      formData.append("comment_text", commentText);
      formData.append("video_id", props.videoId.toString());

      const response = await axios.post(
        API_URL + "comment",
        formData,
        {
          headers: {
            Authorization: `Token ${myToken}`,
            "Content-Type": "multipart/form-data",
          },
        }
      );

      if (response.status === 201) {
        setCommentText("");
        alert('Comment Added');
      } else {
        // Handle error response
        console.error("Failed to submit comment");
        // Display error message to the user
      }
    } catch (error) {
      // Handle network error
      console.error("Network error:", error);
      // Display error message to the user
    }
  };

 
  const handleManyChannelsComment = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if(channelId!==0){
      try {
        const formData = new FormData();
        formData.append("comment_text", commentText);
        formData.append("video_id", props.videoId.toString());
        formData.append("channel_id", channelId.toString());
  
        const response = await axios.post(
          API_URL + "commentManyChannels",
          formData,
          {
            headers: {
              Authorization: `Token ${myToken}`,
              "Content-Type": "multipart/form-data",
            },
          }
        );
  
        if (response.status === 201) {
          setCommentText("");
          alert('Comment Added');
        } else {
          // Handle error response
          console.error("Failed to submit comment");
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
          <form id="comment-form"
          onSubmit={handleComment}
          >
            <fieldset>
            <div className="row">
              <h5>
                <label htmlFor="comment-text">Add Comment</label>
              </h5>
              <textarea
                rows={3}
                cols={140}
                maxLength={500}
                id="comment-text"
                name="comment_text"
                value={commentText}
                onChange={(e) => setCommentText(e.target.value)}
              ></textarea>
            </div>
            <div className="row" style={commentButton}>
              <button className="btn btn-success" type="submit"
              disabled={!commentText}
              >
                Comment
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
          <form
            id="comment-many-channels-form"
            onSubmit={handleManyChannelsComment}
          >
            <fieldset>
            <div className="row">
              <h5>
                <label htmlFor="comment-text">Add Comment</label>
              </h5>
              <textarea
                rows={3}
                cols={140}
                maxLength={500}
                id="comment-text"
                name="comment_text"
                value={commentText}
                onChange={(e) => setCommentText(e.target.value)}
              ></textarea>
            </div>
            <div className="row">
              <div className="col-lg-12">
                <div className="row">
                  <label htmlFor="channel-id">Select channel</label>
                </div>
                <div className="row">
                  <select name="channel_id" id="channel-id" onChange={(e) => setChannelId(Number(e.target.value))}>
                  <option key="select_channel" value={0}>Select Channel</option>
                    {options}
                  </select>
                </div>
              </div>
            </div>
            <div className="row" style={commentButton}>
              <button
                className="btn btn-success"
                type="submit"
                disabled={!commentText || channelId === 0}
              >
                Comment
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
        <h6 className="row box-element">Login to Add Comment</h6>
      </a>
    );
  }
};

export default Commenting;
