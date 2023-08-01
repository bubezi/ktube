import Dropdown from "react-bootstrap/Dropdown";
import imagePlaceholder from "../../assets/images/placeholder.png";
import { Channel } from "../Watchpage";
import { toggleStyle } from "../../assets/styles/Styles";
import axios from "axios";
import { API_URL } from "../../constants";
import React from "react";
import { colorRed, commentDpStyle } from "../../assets/styles/WatchStyles";
import { ChannelDetailsState } from "../Videocard";
import { CommentReply } from "./Comments";

interface Props {
  comment: CommentReply;
  owner: boolean;
  manyChannels: boolean;
  channels: Array<Channel>;
}


const CommentReplyItem = (props: Props) => {
    const channelDetailsState: ChannelDetailsState = {profile_picture:'', name:''};
    const [channelDetails, setChannelDetails] = React.useState<ChannelDetailsState>(channelDetailsState);
  
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
  
    const commentReplyStyle = {
      marginLeft: "30px"
    }
    
    const DeleteComp = () => {
      if (myToken && props.owner) {
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
        <div className="row box-element" style={commentReplyStyle}>
        <div className="col-lg-12">
            <div className="row description">
            <ChannelDp />
            <a href="#">
                <p>
                <strong><small>{channelDetails.name}</small></strong>
                </p>
            </a>
            </div>
            <div className="row description">
            <p><small>{props.comment.reply}</small></p>
            </div>
            <DeleteComp />
        </div>
        </div>
    </>
    );
}

export default CommentReplyItem;
