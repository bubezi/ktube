// import placeholder from '../assets/images/thumbnail-placeholder.webp'
import imagePlaceholder from '../assets/images/placeholder.png'
import axios from 'axios'
import { API_URL } from '../constants'
import React from 'react'

import Videooptions from './Options/Videooptions'

interface Prop {
    videoId: number,
    title: string,
    thumbnail: string,
    channelId: number,
    slug: string,
    price: number,
    views: number,
    colSize: string,
}

export interface ChannelDetailsState {
    profile_picture: string,
    name: string,
}

const Videocard = (props: Prop) => {
    const channelDetailsState: ChannelDetailsState = {profile_picture:'', name:''};
    const [channelDetails, setChannelDetails] = React.useState<ChannelDetailsState>(channelDetailsState);


    React.useEffect(()=>{
        if (props.channelId !== 0){
            axios.get(API_URL+"dp/"+props.channelId)
                .then(res => setChannelDetails(res.data))
                .catch((error)=>{console.log(error)});
        }
    },[props.channelId]);


    const channelDp = `${channelDetails.profile_picture}`;
    const videoChannelName = `${channelDetails.name}`;


    const imageStyle = {
        width: "20px", 
        height: "20px",
    }
    
    const priceStyle = {
        // float: "right", 
        color: "green",
        marginBottom: "0 !important",
    }
    

    const pluralViews = props.views === 1 ? 'view' : 'views';

    const ChannelDP = () => {
        if (props.thumbnail===''){
            return ( <img src={imagePlaceholder} className="channel-icon" alt="Channel Profile picture" style={imageStyle}/>);
        }
        else{
            return ( <img src={channelDp} className="channel-icon" alt="Channel Profile picture" style={imageStyle}/>);                          
        }
    }

    const Price = () => {
        if (props.price>0) {
            return (<p style={priceStyle}>KShs. { props.price }</p>);
        }else{
            return (<></>);
        }
    }
    
    return (
        <>
            <div className={props.colSize}>
                <a href={"/watch/" + props.slug}>
                    <img src={props.thumbnail} alt="thumbnail" className="thumbnail" />
                </a>
                <div className="box-element product">
                    <div className="row">
                        <a href={"/watch/" + props.slug}>
                            <h6>{props.title}</h6>
                        </a>
                    </div>
                    <div className="row">
                        <div className="col-lg-6">
                            <div className="row">
                                <a href={"/channel/" + props.channelId}>
                                    <ChannelDP/>
                                </a>
                                <a href={"/channel/" + props.channelId}>
                                    <h6>{videoChannelName}</h6>
                                </a>
                            </div>
                        </div>
                        <div className="col-lg-6 col-12 text-right mt-2 mt-lg-0">
                            {/* <p style={priceStyle}>KShs. {{ video.price | floatformat:2 | intcomma }}</p> */} 
                            {/* React version of Humanize*/}
                            <Price/>
                        </div>
                    </div>
                    <div className="row">
                        <div className="col-lg-10">
                            <div className="row">
                                <h6 id="video-views">{props.views} {pluralViews}</h6>
                            </div>
                        </div>
                        <div className="col-lg-2 col-12 text-right mt-2 mt-lg-0">
                            <Videooptions videoId={props.videoId}/>
                        </div>
                    </div>
                </div>
            </div>
        </>
    );
}

export default Videocard;