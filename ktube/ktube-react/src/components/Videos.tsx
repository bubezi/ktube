import Videocard from "./Videocard";
import React from "react";
import axios from 'axios'
import { API_URL } from "../constants";

interface VideoState {
    id : number;
    title : string;
    thumbnail : string;
    channel : number;
    views : number;
    slug : string;
    path : string;
    price : number;
}

function Videos() {
  const videoState: Array<VideoState> = [{id:0, title:'', thumbnail:'', channel:0, views:0, slug:'', path:'', price:0.0}]
  const [videos, setVideos] = React.useState<Array<VideoState>>(videoState);

  React.useEffect(()=>{
    axios.get(API_URL+"videos")
        .then(res => setVideos(res.data))
        .catch((error)=>{
          console.log(error);
        })
  },[]);

  
  const videocards = videos.map(video => {
    if (video.channel!==0){
    const videoThumbnail = `${video.thumbnail}`;
    const videoTitle = `${video.title}`;
    const videoChannelId = video.channel;
        
    return  (<Videocard 
              key={video.id} 
              title = {videoTitle} 
              thumbnail={videoThumbnail} 
              channelId={videoChannelId} 
              price={video.price} 
              views={video.views}/>
    );
}})
  


  return (
    <>
        <div className="row">
            { videocards }
        </div>
    </>
  );
}

export default Videos;
