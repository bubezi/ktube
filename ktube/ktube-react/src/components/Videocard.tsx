// import placeholder from '../assets/images/thumbnail-placeholder.webp'
// import imagePlaceholder from '../assets/images/placeholder.png'
import axios from 'axios'
import { API_URL } from '../constants'
import React from 'react'

import Videooptions from './Videooptions'

interface Prop {
    title: string,
    thumbnail: string,
    channelId: number,
    price: number,
    views: number,
}

interface ChannelDetailsState {
    profile_picture: string,
    name: string,
}

function Videocard (props: Prop) {
    const channelDetailsState: ChannelDetailsState = {profile_picture:'', name:''};
    const [channelDetails, setChannelDetails] = React.useState(channelDetailsState);

    axios.get(API_URL+"dp/"+props.channelId)
        .then(res => setChannelDetails(res.data));

    const channelDp = `${channelDetails.profile_picture}`;
    const videoChannelName = `${channelDetails.name}`;

    const pluralViews = props.views === 1 ? 'view' : 'views';


    const videoTitle = {
        // float: "left"
    }

    const imageStyle = {
        width: "20px", 
        height: "20px",
    }

    const priceStyle = {
        // float: "right", 
        color: "green",
        marginBottom: "0 !important",
    }

    return (
        <>
            <div className="col-lg-4">
                <a href="#">
                    <img src={props.thumbnail} alt="thumbnail" className="thumbnail" />
                </a>
                <div className="box-element product">
                    <div className="row">
                        <a href="#">
                            <h6 style={videoTitle}>{props.title}</h6>
                        </a>
                    </div>
                    <div className="row">
                        <div className="col-lg-6">
                            <div className="row">
                                <a href="#">
                                {/* {% if video.channel.profile_picture %} */}
                                <img src={channelDp} className="channel-icon" alt="Channel Profile picture" style={imageStyle}/>
                                {/* {% else %} */}
                                {/* <img src={imagePlaceholder} className="channel-icon" alt="Channel Profile picture" style={imageStyle}/> */}
                                {/* {% endif %} */}
                                </a>
                                <a href="#">
                                    <h6>{videoChannelName}</h6>
                                </a>
                            </div>
                        </div>
                        {/* {% if video.price > 0 %} */}
                        <div className="col-lg-6 col-12 text-right mt-2 mt-lg-0">
                            {/* <p style={priceStyle}>KShs. {{ video.price | floatformat:2 | intcomma }}</p> */}
                            <p style={priceStyle}>KShs. { props.price }</p>
                        </div>
                        {/* {% endif %} */}
                    </div>
                    <div className="row">
                        <div className="col-lg-10">
                            <div className="row">
                                <h6 id="video-views" style={videoTitle}>{props.views} {pluralViews}</h6>
                            </div>
                        </div>
                        <div className="col-lg-2 col-12 text-right mt-2 mt-lg-0">
                            <Videooptions />
                        </div>
                    </div>
                </div>
            </div>
        </>
    );
}

export default Videocard;