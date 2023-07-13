import Navbar from "./Navbar";

function Watchpage () {
    const mainRowStyle = {
        alignItems: "flex-start"
    }
    const mainColStyle = {
        padding: 0,
    }
    return (
        <>
            <Navbar username="bubezi"/>
            <div className="row" style={mainRowStyle}>
                <div className="col-lg-9" style={mainColStyle}>
                    <video 
                    autoPlay
                    preload="auto" 
                    controls>
                    <source src="http://localhost/media/Rust_Absolutely_Positively_Sucks.mp4" type="video/mp4"/>
                    {/* <source src="{{video.videoURL}}" type="video/x-matroska"/>
                    <source src="{{video.videoURL}}" type="video/webm"/> */}
                    Your browser does not support the video
                    </video>
                </div>

            </div>

        </>
    );
}

export default Watchpage;