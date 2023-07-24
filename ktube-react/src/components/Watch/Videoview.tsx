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
        <source src={props.video} type="video/mp4"/>
        <source src={props.video} type="video/x-matroska"/>
        <source src={props.video} type="video/webm"/>
        Your browser does not support the video
        </video>
    </>
    );
}