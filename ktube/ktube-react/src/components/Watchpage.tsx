import Navbar from "./Navbar";

function Watchpage () {
    const mainRowStyle = {
        alignItems: "flex-start"
    }
    const mainColStyle = {
        padding: 0,
    }

    const containerStyle = {
        background: "linear-gradient(Grey, whitesmoke)!important"
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
                    {/* <source src="http://localhost/media/Rust_Absolutely_Positively_Sucks.mp4" type="video/x-matroska"/>
                    <source src="http://localhost/media/Rust_Absolutely_Positively_Sucks.mp4" type="video/webm"/> */}
                    Your browser does not support the video
                    </video>

                    <div className="container" style={containerStyle}></div> 
                </div>
                <div className="col-lg-3"></div>

            </div>



        </>
    );
}

export default Watchpage;