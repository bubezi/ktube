import Dropdown from "react-bootstrap/Dropdown";
import imagePlaceholder from "../../assets/images/placeholder.png";
import { Channel } from "../Watchpage";
import { Comment } from "./Comments";
import { elipsisStyle, toggleStyle } from "../../assets/styles/Styles";
import axios from "axios";
import { API_URL } from "../../constants";
import React from "react";
import { colorRed, commentDpStyle } from "../../assets/styles/WatchStyles";
import { ChannelDetailsState } from "../Videocard";

interface Props {
  comment: Comment;
  manyChannels: boolean;
  channels: Array<Channel>;
}


const Commentitem = (props: Props) => {
  const channelDetailsState: ChannelDetailsState = {profile_picture:'', name:''};
  const [channelDetails, setChannelDetails] = React.useState<ChannelDetailsState>(channelDetailsState);
  const [owner, setOwner] = React.useState<boolean>(false);

  React.useEffect(()=>{
      if (props.comment.channel !== 0){
          axios.get(API_URL+"dp/"+props.comment.channel)
              .then(res => setChannelDetails(res.data))
              .catch((error)=>{console.log(error)});
      }
  }, [props.comment]);

  const [myToken] = React.useState(() => {
    const savedToken = localStorage.getItem("token");
    return savedToken ?? null;
  });
  

  React.useEffect(() => {
    if (myToken !== null && props.comment.channel !== 0) {
      axios({
        method: "get",
        url: API_URL + "isowner/" + String(props.comment.channel),
        headers: {
          Authorization: `Token ${myToken}`,
        },
      })
        .then((res) => {
          const channelOwner = res.data?.is_owner;
          setOwner(channelOwner);
        })
        .catch((error) => {
          console.log(error);
        });
    }
  }, []);

  const commentStyle = {
    marginLeft: "0px"
  }
  
  const DeleteComp = () => {
    if (myToken && owner) {
      return (
        <div className="row">
          <div className="col-lg-10"></div>
          <div className="col-lg-2 col-12 text-right mt-2 mt-lg-0">
          <div className="video-options">
            <div className="dropdown">
              <Dropdown>
                <Dropdown.Toggle
                  id="dropdownMenuButton1"
                  className="custom-dropdown"
                  style={toggleStyle}
                >
                  <i className="fa-solid fa-ellipsis-vertical"
                  style={elipsisStyle}
                  ></i>
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
    if (props.comment.channel === 0) {
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
          src={channelDetails.profile_picture}
          className="channel-icon"
          alt="Channel Profile picture"
          style={commentDpStyle}
        />
      );
    }
  };
    return (
      <>
        <div className="row box-element" style={commentStyle}>
          <div className="col-lg-12">
            <div className="row description">
              <ChannelDp />
              <a href="#">
                <p>
                  <strong>{channelDetails.name}</strong>
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

export default Commentitem;
