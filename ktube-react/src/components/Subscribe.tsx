import React from "react";

import { useViewerContext } from "../providers/ViewerProvider";
import { subOrUnsub } from "../functions/fun";
import { marginLeft40 } from "../assets/styles/WatchStyles";

interface Props {
    subscribers: number[],
    channelId: number,
    channelUserId: number,
    setSubscriberCount:  React.Dispatch<React.SetStateAction<number>>,
    subscriberCount: number,
}

const Subscribe = (props: Props) => {
    const viewerProvided = useViewerContext();
    const [ subscribed, setSubscribed ] = React.useState(props.subscribers.includes(viewerProvided.viewer.id) && viewerProvided.viewer.id !== 0);
    const [myToken] = React.useState(() => {
      const savedToken = localStorage.getItem("token");
      return savedToken ?? null;
    });

      React.useEffect(() => {
        setSubscribed(props.subscribers.includes(viewerProvided.viewer.id) && viewerProvided.viewer.id !== 0);
      }, [props.subscribers, viewerProvided.viewer.id]);


    if (myToken){
        const subscribe = () => {
            subOrUnsub('subscribeAPI',  props.channelId, viewerProvided.viewer.id, myToken);
            props.setSubscriberCount(props.subscriberCount + 1);
            setSubscribed(true);
        }
    
        const unSubscribe = () => {
            subOrUnsub('unSubscribeAPI',  props.channelId, viewerProvided.viewer.id, myToken);
            props.setSubscriberCount(props.subscriberCount - 1);
            setSubscribed(false);
        }

        if (viewerProvided.viewer.id === props.channelUserId){
            return (
                <>
                <div className="row">
                    <div className="row"><h6><a href={"/editChannel/" + String(props.channelId)}><button 
                        className="btn btn-outline-secondary add-btn update-cart"
                        style={marginLeft40}>Edit Channel</button></a></h6></div>                
                </div>
                </>
            );

        }else{
            if (!subscribed) {
                return (
                    <>
                    <div className="row">
                        <button className="btn btn-success"
                        style={marginLeft40} type="submit" id="subscribe-button"
                        onClick={subscribe}>Subscribe</button>
                    </div>
                    </>
                );
            }else {
                return (
                    <>
                    <div className="row">
                        <button className="btn btn-outline-secondary add-btn update-cart"
                        style={marginLeft40}  type="submit" id="unsubscribe-button"
                        onClick={unSubscribe}>Unsubscribe</button>  
                    </div>
                    </>
                );
            }
        }

    }else{
        return (
            <>
            <div className="row">
                <a href="/auth/login" target="_blank">
                    <button
                    className="btn btn-success"
                    style={marginLeft40}>Subscribe</button>
                </a>
            </div>
            </>
        );
    }
}

export default Subscribe;
