import React from "react";
import axios from "axios";
import { API_URL } from "../../constants";
import { useViewerContext } from "../../providers/ViewerProvider";
import { likeunlikeOrdislikeUndislike } from "../../functions/fun";
import { marginLeft0 } from "../../assets/styles/WatchStyles";

interface Props {
  likes: number;
  dislikes: number;
  videoId: number;
}

interface PropsButtons {
  videoId: number;
  setLikes: React.Dispatch<React.SetStateAction<number>>,
  likes: number,
  setDisLikes: React.Dispatch<React.SetStateAction<number>>,
  disLikes: number,
}


const Likeanddislikebuttons = (props: PropsButtons) => {
  const viewerProvided = useViewerContext();
  const [liked, setLiked] = React.useState<boolean>(false);
  const [disLiked, setDisLiked] = React.useState<boolean>(false);
  const myToken = useViewerContext().myToken;

  if (myToken) {


  React.useEffect(() => {
    if (props.videoId !== 0 ) {
      axios({
        method: "get",
        url: API_URL + "liked/" + String(props.videoId),
        headers: {
          Authorization: `Token ${myToken}`,
        },
      })
        .then((res) => setLiked(res.data.liked))
        .catch((error) => {
          console.log(error);
        });
  
      axios({
        method: "get",
        url: API_URL + "disliked/" + String(props.videoId),
        headers: {
          Authorization: `Token ${myToken}`,
        },
      })
        .then((res) => setDisLiked(res.data.disliked))
        .catch((error) => {
          console.log(error);
        });
      }
    }, [props.videoId]);


    const like = () => {
      likeunlikeOrdislikeUndislike(
        "likeVideo",
        props.videoId,
        viewerProvided.viewer.id,
        myToken
      );
      props.setLikes(props.likes+1);
      setLiked(true);
    };

    const disLike = () => {
      likeunlikeOrdislikeUndislike(
        "disLikeVideo",
        props.videoId,
        viewerProvided.viewer.id,
        myToken
        );
      props.setDisLikes(props.disLikes+1);
      setDisLiked(true);
    };

    const unLike = () => {
      likeunlikeOrdislikeUndislike(
        "unLikeVideo",
        props.videoId,
        viewerProvided.viewer.id,
        myToken
      );
      props.setLikes(props.likes-1);
      setLiked(false);
    };

    const unDisLike = () => {
      likeunlikeOrdislikeUndislike(
        "unDisLikeVideo",
        props.videoId,
        viewerProvided.viewer.id,
        myToken
      );
      props.setDisLikes(props.disLikes-1);
      setDisLiked(false);
    };

    const LikeButton = () => {
      return (
        <button
          className="btn btn-outline-secondary add-btn update-cart"
          style={marginLeft0}
          type="submit"
          id="like-button"
          onClick={like}
        >
          <i className="fa-regular fa-thumbs-up"></i>
        </button>
      );
    };

    const UnLikeButton = () => {
      return (
        <button
          className="btn btn-outline-secondary add-btn update-cart"
          style={marginLeft0}
          type="submit"
          id="unlike-button"
          onClick={unLike}
        >
          <i className="fa-solid fa-thumbs-up"></i>
        </button>
      );
    };

    const DislikeButton = () => {
      return (
        <button
          className="btn btn-outline-secondary add-btn update-cart"
          style={marginLeft0}
          type="submit"
          id="dislike-button"
          onClick={disLike}
        >
          <i className="fa-regular fa-thumbs-up fa-flip-vertical"></i>
        </button>
      );
    };

    const UnDislikeButton = () => {
      return (
        <button
          className="btn btn-outline-secondary add-btn update-cart"
          style={marginLeft0}
          type="submit"
          id="undislike-button"
          onClick={unDisLike}
        >
          <i className="fa-solid fa-thumbs-down"></i>
        </button>
      );
    };

    if (liked) {
      if (disLiked) {
        return (
          <>
            <div className="row">
              <UnLikeButton />
              <UnDislikeButton />
            </div>
          </>
        );
      } else {
        return (
          <>
            <div className="row">
              <UnLikeButton />
              <DislikeButton />
            </div>
          </>
        );
      }
    } else {
      if (disLiked) {
        return (
          <>
            <div className="row">
              <LikeButton />
              <UnDislikeButton />
            </div>
          </>
        );
      } else {
        return (
          <>
            <div className="row">
              <LikeButton />
              <DislikeButton />
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
            <button
              className="btn btn-outline-secondary add-btn update-cart"
              style={marginLeft0}
            >
              <i className="fa-regular fa-thumbs-up"></i>
            </button>
          </a>
          <a href="/auth/login" target="_blank">
            <button
              className="btn btn-outline-secondary add-btn update-cart"
              style={marginLeft0}
            >
              <i className="fa-regular fa-thumbs-up fa-flip-vertical"></i>
            </button>
          </a>
        </div>
      </>
    );
  }
};

const Likeanddislike = (props: Props) => {
  const [ likes, setLikes ] = React.useState<number>(props.likes)
  const [ disLikes, setDisLikes ] = React.useState<number>(props.dislikes)

  React.useEffect(()=>{
    setLikes(props.likes);
    setDisLikes(props.dislikes);
  }, [props.likes, props.dislikes])

  const Likes = () => {
    if (likes === 1) {
      return (
        <h6>
          <strong id="likes-count">{likes} like</strong>
        </h6>
      );
    } else {
      return (
        <h6>
          <strong id="likes-count">{likes} likes</strong>
        </h6>
      );
    }
  };
  const DisLikes = () => {
    if (disLikes === 1) {
      return (
        <h6>
          <strong id="dislikes-count">{disLikes} dislike</strong>
        </h6>
      );
    } else {
      return (
        <h6>
          <strong id="dislikes-count">{disLikes} dislikes</strong>
        </h6>
      );
    }
  };
  return (
    <>
      <div className="row">
        <Likes/>
        <DisLikes />
      </div>
      <Likeanddislikebuttons videoId={props.videoId} setLikes={setLikes} likes={likes} setDisLikes={setDisLikes} disLikes={disLikes}/>
    </>
  );
}

export default Likeanddislike;
