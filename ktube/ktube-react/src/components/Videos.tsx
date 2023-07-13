import Videocard from './Videocard'
import React from 'react'
// import axios from 'axios'

// interface Video {
//     id : Int32Array;
//     title : String;
//     video : String;
//     thumbnail : String;
//     description : String;
//     upload_time : String;
//     channel : String;
//     private : Boolean;
//     unlisted : Boolean;
//     likes : Int32Array;
//     dislikes : Int32Array;
//     views : Int32Array;
//     slug : String;
//     path : String;
//     price : Float32Array;
//     paid_viewers : String;
// } 

function Videos () {

    const [videos, setVideos] = React.useState([
        {
            title:"My video",
            channel:"Bubezi",
            price:20,
            views:1022,
        }
    ])


    const fetchdata = () => {
        fetch("http://localhost:8000/api/videos")
            .then(response => response.json())
            .then(data => setVideos(data))
    }

    React.useEffect(() => {
        fetchdata();
    })

    // axios.get("http://localhost:8000/api/videos")
    //     .then(res => setVideos(res.data))

    const videocards = videos.map(video => {
        const videoTitle = `${video.title}`
        const videoChannel = `${video.channel}`
        const videoPrice = `${video.price}`
        const videoViews = `${video.views}`
        return  <Videocard title = {videoTitle} channel={videoChannel} price={videoPrice} views={videoViews}/>
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