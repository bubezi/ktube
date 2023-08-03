import React from "react";
import { commentButton } from "../../assets/styles/WatchStyles";
import { Channel } from "../Watchpage";



interface Props {
  videoId: number;
  channels: Channel[];
  manyChannels: Boolean;
}

const Commenting = (props: Props) => {
  const [myToken] = React.useState(() => {
    const savedToken = localStorage.getItem("token");
    return savedToken ?? null;
  });

  if (myToken) {
    if (!props.manyChannels) {
      return (
        <>
          <form id="comment-form" method="post">
            {/* {% csrf_token %} */}
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
              ></textarea>
            </div>
            <input type="hidden" name="video_id" value="{{video.slug}}" />
            <div className="row" style={commentButton}>
              <button className="btn btn-success" type="submit">
                Comment
              </button>
            </div>
          </form>
        </>
      );
    } else {
      const options = channels.map((channel) => {
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
            method="post"
            encType="multipart/form-data"
          >
            {/* {% csrf_token %} */}
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
              ></textarea>
            </div>
            <input type="hidden" name="video_id" value={props.videoId} />
            <div className="row">
              <div className="col-lg-12">
                <div className="row">
                  <label htmlFor="channel-id">Select channel</label>
                </div>
                <div className="row">
                  <select name="channel_id" id="channel-id">
                    {options}
                  </select>
                </div>
              </div>
            </div>
            <div className="row" style={commentButton}>
              <button className="btn btn-success" type="submit"
            //   onClick={}
              >
                Comment
              </button>
            </div>
          </form>
          <br />
        </>
      );
    }
  } else {
    return (
      <a href="/auth/login" target="_blank">
        <h6 className="row box-element">
          Login to Add Comment
        </h6>
      </a>
    );
  }
};

export default Commenting;
