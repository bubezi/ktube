import Videooptions from "../Options/Videooptions";

interface Props {
    videoId: number,
    views: number,
}

const Viewsandoptions = (props: Props) => {
    const Views = () => {
        if (props.views === 1){
            // <h6><strong id="video-views-count"> {{video.views | intcomma }} views</strong></h6>
            return (<h6><strong id="video-views-count"> {props.views} view</strong></h6>);
        }else{
            return (<h6><strong id="video-views-count"> {props.views} views</strong></h6>);
        }
    }
    return (
    <><div className="row">
    <div className="col-lg-10">
        <div className="row">
            <Views/>
        </div>
    </div>
    
    <div className="col-lg-2 col-12 text-right mt-2 mt-lg-0">
        <Videooptions videoId={props.videoId}/>
    </div>
</div>
    </>
    );
}

export default Viewsandoptions;
