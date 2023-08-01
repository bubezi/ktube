import { API_BASE_URL } from "../../constants";

interface Prop {
    video: string,
}

const Videoview: React.FC<Prop> = ({ video }) => {
    const videoUrl = API_BASE_URL + video;

    return (
        <video 
            autoPlay
            preload="auto" 
            controls
            // alt="Video content"
            >
            <source key="mp4" src={videoUrl} type="video/mp4"/>
            <source key="webm" src={videoUrl} type="video/webm"/>
            {/* <source key="matroska" src={videoUrl} type="video/x-matroska"/> */}
            Your browser does not support the video
        </video>
    );
}

export default Videoview;
