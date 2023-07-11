import placeholder from '../assets/thumbnail-placeholder.webp'
import imagePlaceholder from '../assets/placeholder.png'

interface Prop {
    title: String,
    channel: String,
    price: String,
    views: String
}

function Column (props:Prop) {
    const videoTitle = {
        // float: "left"
    }

    const imageStyle = {
        width: "20px", 
        height: "20px",
    }

    const priceStyle = {
        // float: "right", 
        color: "green",
        marginBottom: "0 !important",
    }

    return (
        <>
            <div className="col-lg-4">
                <a href="#">
                    <img src={placeholder} alt="thumbnail" className="thumbnail" />
                </a>
                <div className="box-element product">
                    <div className="row">
                        <a href="#">
                            <h6 style={videoTitle}>{props.title}</h6>
                        </a>
                    </div>
                    <div className="row">
                        <div className="col-lg-6">
                            <div className="row">
                                <a href="#">
                                {/* {% if video.channel.profile_picture %} */}
                                {/* <img src="#" className="channel-icon" alt="Channel Profile picture" style={imageStyle}/> */}
                                {/* {% else %} */}
                                <img src={imagePlaceholder} className="channel-icon" alt="Channel Profile picture" style={imageStyle}/>
                                {/* {% endif %} */}
                                </a>
                                <a href="#">
                                    <h6>{props.channel}</h6>
                                </a>
                            </div>
                        </div>
                        {/* {% if video.price > 0 %} */}
                        <div className="col-lg-6 col-12 text-right mt-2 mt-lg-0">
                            {/* <p style={priceStyle}>KShs. {{ video.price | floatformat:2 | intcomma }}</p> */}
                            <p style={priceStyle}>KShs. { props.price }</p>
                        </div>
                        {/* {% endif %} */}
                    </div>
                    <div className="row">
                        <div className="col-lg-10">
                            {/* {% if video.views is not 1 %} */}
                                {/* <h6 style={videoTitle}>{{video.views | intcomma }} views</h6> */}
                            {/* {% else %} */}
                                <h6 style={videoTitle}>{props.views} view</h6>
                            {/* {% endif %} */}
                        </div>
                        <div className="col-lg-2 col-12 text-right mt-2 mt-lg-0"></div>
                    </div>
                </div>
            </div>
        </>
    );
}

function Videos () {
    return (
        <>
            <div className="row">
                <Column title="My video" channel="Prince Bubezi" price="120.2" views="120"/>
                <Column title="My video" channel="Prince Bubezi" price="120.2" views="120"/>
                <Column title="My video" channel="Prince Bubezi" price="120.2" views="120"/>
            </div>
        </>
    );
}

export default Videos;