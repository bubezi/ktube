import Videocard from "./Videocard";
import React from "react";
import axios from 'axios'
import { API_URL } from "../constants";

interface VideoState {
    id : number;
    title : string;
    thumbnail : string;
    channel : string;
    views : number;
    slug : string;
    path : string;
    price : number;
}

function Videos() {
  const videoState: Array<VideoState> = [{id:0, title:'', thumbnail:'', channel:'', views:0, slug:'', path:'', price:0.0}]
  const [videos, setVideos] = React.useState(videoState);

  axios.get(API_URL+"videos")
      .then(res => setVideos(res.data))

  
  const videocards = videos.map(video => {
    const videoThumbnail = `${video.thumbnail}`
    const videoTitle = `${video.title}`
    const videoChannelId = `${video.channel}`
    const videoPrice = `${video.price}`
    const videoViews = `${video.views}`
        
    return  <Videocard title = {videoTitle} thumbnail={videoThumbnail} channelId={videoChannelId} price={videoPrice} views={videoViews}/>
  })
  


  return (
    <>
        <div className="row">
            { videocards }
        </div>
    </>
  );
}

export default Videos;
