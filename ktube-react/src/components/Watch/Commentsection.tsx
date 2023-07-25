import imagePlaceholder from "../../assets/images/placeholder.png";
import { Channel } from "../Watchpage";
import { Comment } from "./Comments";

interface Props {
  comment: Comment;
  manyChannels: boolean;
  channels: Array<Channel>;
}

export default function Commentsection(props: Props) {
  const ChannelDp = () => {
    if (props.comment.channel_dp === "") {
      return (
        <img
          src={imagePlaceholder}
          className="channel-icon"
          alt="Channel Profile picture"
          style={commentDpStyle}
        />
      );
    } else {
      return (
        <img
          src={props.comment.channel_dp}
          className="channel-icon"
          alt="Channel Profile picture"
          style={commentDpStyle}
        />
      );
    }
  };
  return (
    <>
      <div className="row box-element">
        <div className="col-lg-12">
          <div className="row description">
            <ChannelDp />
            <a href="{% url 'channel' comment.channel.id %}">
              <p>
                <strong>{props.comment.channel}</strong>
              </p>
            </a>
          </div>
          <div className="row description">
            <p>{props.comment.comment_text}</p>
          </div>
          <div className="row">
            <div className="video-options">
              <div className="dropdown">
                <button
                  className="btn"
                  type="button"
                  id="dropdownMenuButton1"
                  data-toggle="dropdown"
                  aria-haspopup="true"
                  aria-expanded="true"
                >
                  <i className="fa-solid fa-ellipsis-vertical"></i>
                </button>

                <div
                  className="dropdown-menu dropdown-menu-right"
                  aria-labelledby="dropdownMenuButton1"
                >
                  <a
                    className="dropdown-item"
                    style={colorRed}
                    // onClick={"event.preventDefault(); deleteComment(event, '{{comment.id}}');"}
                  >
                    Delete Comment
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
