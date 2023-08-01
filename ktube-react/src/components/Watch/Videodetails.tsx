import imagePlaceholder from '../../assets/images/placeholder.png'
import Subscribe from '../Subscribe';
import Viewsandoptions from './Viewsandoptions';
import Likeanddislike from "./Likeanddislike";
import Description from './Description';
import { channelStyle, dpStyle, publicityStyle, titleStyle } from '../../assets/styles/WatchStyles';
import { API_BASE_URL } from '../../constants';


interface Prop {
    title: string,
    channel: string,
    subscriber_count: number,
    private: boolean,
    unlisted: boolean,
    profile_picture: string,
    channelId: number,
    subscribers: number[],
    channelUserId: number,
    videoId: number,
    views: number,
    likes: number,
    dislikes: number,
    description: string,
    upload_time: string,
}

const brStyle = {
    
}

const Videodetails = (props: Prop) => {
    const PrivateOrUnlisted = () => {
        if (props.private){
            return (<h6 style={publicityStyle}>(private)</h6>);
        }else {
            if (props.unlisted){
                return (<h6 style={publicityStyle}>(unlisted)</h6>);
            }
        }
    }

    const Profilepicture = () => {
        if (props.profile_picture !== ''){
            return (<img src={API_BASE_URL + props.profile_picture} className="channel-icon" alt="Channel Profile picture" style={dpStyle}/>);
        }else{
            return (<img src={imagePlaceholder} className="channel-icon" alt="Channel Profile picture placeholder" style={dpStyle}/>);
        }
    }

    const Subscribercount = () => {
        if (props.subscriber_count === 1){
            return (<h5 id='subscriber-count' style={publicityStyle}>{props.subscriber_count } Subscriber</h5>);
        }else{
            return (<h5 id='subscriber-count' style={publicityStyle}>{props.subscriber_count } Subscribers</h5>);
        }
    }

    return (
    <>
        <div className="row box-element">
            <div className="col-lg-12">  
                <div className="row">
                    <div className="col-lg-12">
                        <div className="row">
                            <h6 style={titleStyle}><strong>{props.title}</strong></h6>
                            <PrivateOrUnlisted/>
                        </div>
                        <div className="row">
                            <Profilepicture/>
                            <a href={"/channel/" + String(props.channelId)}>
                                <h6 style={channelStyle}><strong>{props.channel}</strong></h6>
                            </a>
                            <h5 style={publicityStyle}>-</h5>
                            <Subscribercount/>
                        </div>
                    </div>
                </div>
                <Subscribe subscribers={props.subscribers} channelId={props.channelId} channelUserId={props.channelUserId}/>
                <br style={brStyle}/>
                <Viewsandoptions videoId={props.videoId} views={props.views}/>
                <br style={brStyle}/>
                <Likeanddislike videoId={props.videoId} likes={props.likes} dislikes={props.dislikes}/>
                <Description description={props.description} upload_time={props.upload_time}/>
                <br/>
            </div>
        </div>
    </>
    );
}

export default Videodetails;
