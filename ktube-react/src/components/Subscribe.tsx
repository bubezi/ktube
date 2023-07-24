import React from "react";

import { useViewerContext } from "../providers/ViewerProvider";
import { subOrUnsub } from "../functions/fun";

interface Props {
    subscribers: number[],
    channelId: number,
    channelUserId: number,
}

export default function Subscribe (props: Props) {
    const [ subscribed, setSubscribed ] = React.useState(props.subscribers.includes(props.channelUserId));
    const [myToken] = React.useState(() => {
      const savedToken = localStorage.getItem("token");
      return savedToken ?? null;
    });

    const viewerProvided = useViewerContext();

    if (myToken){
        const subscribe = () => {
            subOrUnsub('subscribeAPI',  props.channelId, viewerProvided.viewer.id, myToken);
            setSubscribed(true);
        }
    
        const unSubscribe = () => {
            subOrUnsub('unSubscribeAPI',  props.channelId, viewerProvided.viewer.id, myToken);
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