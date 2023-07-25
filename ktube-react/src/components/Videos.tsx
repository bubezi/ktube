import Videocard from "./Videocard";
import React from "react";
import axios from 'axios'
import { API_URL } from "../constants";

export interface VideoType {
    id : number;
    title : string;
    thumbnail : string;
    channel : number;
    views : number;
    slug : string;
    path : string;
    price : number;
}

export const videoInit: Array<VideoType> = [{id:0, title:'', thumbnail:'', channel:0, views:0, slug:'', path:'', price:0.0}]

function Videos() {
  const [videos, setVideos] = React.useState<Array<VideoType>>(videoInit);

  React.useEffect(()=>{
    axios.get(API_URL+"homevideos")
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
              videoId={video.id}
              title = {videoTitle} 
              thumbnail={videoThumbnail} 
              channelId={videoChannelId} 
              slug={video.slug}
              price={video.price} 
              views={video.views}
              colSize="col-lg-4"
              />
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
