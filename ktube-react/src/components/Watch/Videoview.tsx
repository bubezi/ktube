import { IMAGES_URL } from "../../constants";

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
        <source src={IMAGES_URL + props.video} type="video/mp4"/>
        <source src={IMAGES_URL + props.video} type="video/x-matroska"/>
        <source src={IMAGES_URL + props.video} type="video/webm"/>
        Your browser does not support the video
        </video>
    </>
    );
}