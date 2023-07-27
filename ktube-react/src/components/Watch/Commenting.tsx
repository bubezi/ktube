import React from "react";
import axios from "axios";
import { API_URL } from "../../constants";
import { useViewerContext } from "../../providers/ViewerProvider";
import { Channel } from "../Watchpage";
import { commentButton } from "../../assets/styles/WatchStyles";
// import { channelInit } from "../Watchpage";

const channelInit = { id:0, name: "", profile_picture: "", subscriber_count: 0, private: true, unlisted:true, subscribers:[0], userId:0};

const channelsInit = [channelInit]

interface Props {
    videoId: number,
}

export default function Commenting (props: Props) {
    const viewerProvided = useViewerContext();
    const [ manyChannels, setManyChannels ] = React.useState<boolean>(false)
    const [ channels, setChannels ] = React.useState<Array<Channel>>(channelsInit)
    const [myToken] = React.useState(() => {
      const savedToken = localStorage.getItem("token");
      return savedToken ?? null;
    });

    React.useEffect(()=>{
        if (viewerProvided.viewer.id !== 0){
            axios({
              method: "get",
              url: API_URL + "getChannels/" + String(viewerProvided.viewer.id),
              headers: {
                Authorization: `Token ${myToken}`,
              },
            })
              .then((res) => {
                setChannels(res.data);
                if(channels.length>1){setManyChannels(true)};})
              .catch((error) => {
                console.log(error);
              });
        }
      }, []);
      
    if (myToken) {
        if (!manyChannels){
            return (
            <>
            <form id="comment-form" method="post">
                {/* {% csrf_token %} */}
                <div className="row">
                    <h5><label htmlFor="comment-text">Add Comment</label></h5>
                    <textarea rows={3} cols={140} maxLength={500} id="comment-text" name="comment_text"></textarea>
                </div>
                <input type="hidden" name="video_id" value="{{video.slug}}"/>
                <div className="row" style={commentButton}>
                    <button className="btn btn-success" type="submit">Comment</button>
                </div>
            </form>
            </>
            );
        }else{
            const options = channels.map((channel)=>{
                const value = `${channel.id}`
                const name = `${channel.name}`
                return (<option key={channel.id} value={value}>{name}</option>);
            })
            return (
                <>
                    <form id="comment-many-channels-form" method="post">
                        {/* {% csrf_token %} */}
                        <div className="row">
                            <h5><label htmlFor="comment-text">Add Comment</label></h5>
                            <textarea rows={3} cols={140} maxLength={500} id="comment-text" name="comment_text"></textarea>
                        </div>
                        <input type="hidden" name="video_id" value={props.videoId}/>
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
                            <button className="btn btn-success" type="submit">Comment</button>
                        </div>
                    </form>
                    <br/>
                </>
            );
        }
    }else{
        return (<a href="/auth/login" target="_blank"><h6 className="row box-element"><u>Login</u> to Add Comment</h6></a>);
    }
}