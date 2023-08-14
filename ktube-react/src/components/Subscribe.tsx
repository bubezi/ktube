import React, { CSSProperties } from "react";

import { useViewerContext } from "../providers/ViewerProvider";
import { subOrUnsub } from "../functions/fun";

interface Props {
  subscribers: number[];
  channelId: number;
  channelUserId: number;
  setSubscriberCount: React.Dispatch<React.SetStateAction<number>>;
  subscriberCount: number;
  marginLeft: CSSProperties;
}

const Subscribe = (props: Props) => {
  const viewerProvided = useViewerContext();
  const myToken = viewerProvided.myToken;
  const [subscribed, setSubscribed] = React.useState(
    props.subscribers.includes(viewerProvided.viewer.id) &&
      viewerProvided.viewer.id !== 0
  );

  React.useEffect(() => {
    setSubscribed(
      props.subscribers.includes(viewerProvided.viewer.id) &&
        viewerProvided.viewer.id !== 0
    );
  }, [props.subscribers, viewerProvided.viewer.id]);

  if (myToken) {
    const subscribe = () => {
      setSubscribed(true);
      subOrUnsub(
        "subscribeAPI",
        props.channelId,
        viewerProvided.viewer.id,
        myToken
      );
      props.setSubscriberCount(props.subscriberCount + 1);
    };

    const unSubscribe = () => {
      setSubscribed(false);
      subOrUnsub(
        "unSubscribeAPI",
        props.channelId,
        viewerProvided.viewer.id,
        myToken
      );
      props.setSubscriberCount(props.subscriberCount - 1);
    };

    if (viewerProvided.viewer.id === props.channelUserId) {
      return (
        <>
          <div className="row">
            <div className="row">
              <h6>
                <a href={"/editChannel/" + String(props.channelId)}>
                  <button
                    className="btn btn-outline-secondary add-btn update-cart"
                    style={props.marginLeft}
                  >
                    Edit Channel
                  </button>
                </a>
              </h6>
            </div>
          </div>
        </>
      );
    } else {
      if (!subscribed) {
        return (
          <>
            <div className="row">
              <button
                className="btn btn-success"
                style={props.marginLeft}
                type="submit"
                id="subscribe-button"
                onClick={subscribe}
              >
                Subscribe
              </button>
            </div>
          </>
        );
      } else {
        return (
          <>
            <div className="row">
              <button
                className="btn btn-outline-secondary add-btn update-cart"
                style={props.marginLeft}
                type="submit"
                id="unsubscribe-button"
                onClick={unSubscribe}
              >
                Unsubscribe
              </button>
            </div>
          </>
        );
      }
    }
  } else {
    return (
      <>
        <div className="row">
          <a href="/auth/login" target="_blank">
            <button className="btn btn-success" style={props.marginLeft}>
              Subscribe
            </button>
          </a>
        </div>
      </>
    );
  }
};

export default Subscribe;
