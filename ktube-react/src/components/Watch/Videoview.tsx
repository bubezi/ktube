import { API_BASE_URL } from "../../constants";

interface Prop {
    video: string,
}

export default function Videoview (props: Prop) {
    return (
    <>
        <video 
        autoPlay
        preload="auto" 
        controls>
        <source src={API_BASE_URL + props.video} type="video/mp4"/>
        <source src={API_BASE_URL + props.video} type="video/x-matroska"/>
        <source src={API_BASE_URL + props.video} type="video/webm"/>
        Your browser does not support the video
        </video>
    </>
    );
}