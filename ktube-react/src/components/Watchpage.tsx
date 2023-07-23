import React from "react";
import { useParams } from "react-router-dom"

interface Prop {
    title: string,
    channel: string,
    subscriber_count: number
}

function Watchpage (props: Prop) {
    const { slug } = useParams();

    React.useEffect(() => {
        // Fetch data from Django backend using `slug`
      }, [slug]);

    const mainRowStyle = {
        alignItems: "flex-start"
    }
    const mainColStyle = {
        padding: 0,
    }

    const containerStyle = {
        background: "linear-gradient(Grey, whitesmoke)!important"
    }

    const titleStyle = {
        fontSize: "25px"
    }

    const publicityStyle = {
        paddingLeft: "10px"
    }

    const dpStyle = {
        width: "30px",
        height: "30px"
    }

    const channelStyle = {
        fontSize: "20px"
    }


    return (
        <>
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

                    <div className="container" style={containerStyle}>
                        <div className="row box-element">
                            <div className="col-lg-12">  
                                <div className="row">
                                    <div className="col-lg-12">
                                        <div className="row">
                                            <h6 style={titleStyle}><strong>{props.title}</strong></h6>
                                            {/* {% if video.private %} */}
                                            {/* <h6 style={publicityStyle}>(private)</h6> */}
                                            {/* {% elif video.unlisted %} */}
                                            <h6 style={publicityStyle}>(unlisted)</h6>
                                            {/* {% endif %} */}

                                        </div>
                                        <div className="row">
                                            {/* {% if video.channel.profile_picture %} */}
                                            <img src="#" className="channel-icon" alt="Channel Profile picture" style={dpStyle}/>
                                            {/* {% else %} */}
                                            <img src="#" className="channel-icon" alt="Channel Profile picture" style={dpStyle}/>
                                            {/* {% endif %} */}
                                            <a href="#">
                                                <h6 style={channelStyle}><strong>{props.channel}</strong></h6>
                                            </a>
                                            <h5 style={publicityStyle}>-</h5>
                                            {/* {% if props.subscriber_count  == 1 %}<h5 id='subscriber-count' style={publicityStyle}>{props.subscriber_count } Subscriber</h5>{% else %} */}
                                            <h5 id='subscriber-count' style={publicityStyle}>{props.subscriber_count } Subscribers</h5>
                                            {/* {% endif %} */}
                                        </div>
                                    </div>
                                </div>
                            </div>

                        </div>

                    </div>

                </div>
                <div className="col-lg-3"></div>
            </div>
        </>
    );
}

export default Watchpage;