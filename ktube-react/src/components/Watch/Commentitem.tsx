import Dropdown from "react-bootstrap/Dropdown";
import imagePlaceholder from "../../assets/images/placeholder.png";
import { Channel } from "../Watchpage";
import { Comment } from "./Comments";
import { toggleStyle } from "../../assets/styles/Styles";
import axios from "axios";
import { API_URL } from "../../constants";
import React from "react";

interface Props {
  comment: Comment;
  manyChannels: boolean;
  channels: Array<Channel>;
}

export default function Commentitem(props: Props) {
  const [owner, setOwner] = React.useState<boolean>(false);
  const [myToken] = React.useState(() => {
    const savedToken = localStorage.getItem("token");
    return savedToken ?? null;
  });

  React.useEffect(() => {
    axios({
      method: "get",
      url: API_URL + "isowner/" + String(props.comment.id),
      headers: {
        Authorization: `Token ${myToken}`,
      },
    })
      .then((res) => setOwner(res.data.is_owner))
      .catch((error) => {
        console.log(error);
      });    
  }, [myToken]);

  const DeleteComp = () => {
    if (myToken && owner) {
      return (
        <div className="row">
          <div className="video-options">
            <div className="dropdown">
              <Dropdown>
                <Dropdown.Toggle
                  id="dropdownMenuButton1"
                  className="custom-dropdown"
                  style={toggleStyle}
                  aria-haspopup="true"
                  aria-expanded="true"
                >
                  <i className="fa-solid fa-ellipsis-vertical"></i>
                </Dropdown.Toggle>
                <Dropdown.Menu>
                  <Dropdown.Item
                    className="dropdown-item"
                    style={colorRed}
                    onClick={deleteComment}
                  >
                    Delete Comment
                  </Dropdown.Item>
                </Dropdown.Menu>
              </Dropdown>
            </div>
          </div>
        </div>
      );
    }
  };

  const deleteComment = () => {
    const data = {
      commentId: props.comment.id,
    };

    const config = {
      headers: {
        "Content-Type": "application/json",
        Authorization: `Token ${myToken}`,
      },
    };

    axios
      .post(API_URL + "deleteComment", data, config)
      .then((response) => {
        console.log(response.data);
      })
      .catch((error) => {
        if (error.response) {
          console.log(error.response.data);
          console.log(error.response.status);
          console.log(error.response.headers);
        } else if (error.request) {
          console.log(error.request);
        } else {
          console.log("Error", error.message);
        }
        console.log(error.config);
      });
  };

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
          <DeleteComp />
        </div>
      </div>
    </>
  );
}
