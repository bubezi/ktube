import React from "react";
import axios from "axios";
import { API_URL } from "../../constants";
import { useViewerContext } from "../../providers/ViewerProvider";
import { likeunlikeOrdislikeUndislike } from "../../functions/fun";

interface Props {
  likes: number;
  dislikes: number;
  videoId: number;
}

interface PropsButtons {
  videoId: number;
}

const viewerProvided = useViewerContext();

const Likeanddislikebuttons = (props: PropsButtons) => {
  const [liked, setLiked] = React.useState<boolean>(false);
  const [disLiked, setDisLiked] = React.useState<boolean>(false);
  const [myToken] = React.useState(() => {
    const savedToken = localStorage.getItem("token");
    return savedToken ?? null;
  });

  React.useEffect(() => {
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
  }, []);

  if (myToken) {
    const like = () => {
      likeunlikeOrdislikeUndislike(
        "likeVideo",
        props.videoId,
        viewerProvided.viewer.id,
        myToken
      );
      setLiked(true);
    };

    const disLike = () => {
      likeunlikeOrdislikeUndislike(
        "disLikeVideo",
        props.videoId,
        viewerProvided.viewer.id,
        myToken
      );
      setDisLiked(true);
    };

    const unLike = () => {
      likeunlikeOrdislikeUndislike(
        "unLikeVideo",
        props.videoId,
        viewerProvided.viewer.id,
        myToken
      );
      setLiked(false);
    };

    const unDisLike = () => {
      likeunlikeOrdislikeUndislike(
        "unDisLikeVideo",
        props.videoId,
        viewerProvided.viewer.id,
        myToken
      );
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
          <a href="{% url 'login' %}" target="_blank">
            <button
              className="btn btn-outline-secondary add-btn update-cart"
              style={marginLeft0}
            >
              <i className="fa-regular fa-thumbs-up"></i>
            </button>
          </a>
          <a href="{% url 'login' %}" target="_blank">
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

export default function Likeanddislike(props: Props) {
  const Likes = () => {
    if (props.likes === 1) {
      return (
        <h6>
          <strong id="likes-count">{props.likes} like</strong>
        </h6>
      );
    } else {
      return (
        <h6>
          <strong id="likes-count">{props.likes} likes</strong>
        </h6>
      );
    }
  };
  const DisLikes = () => {
    if (props.dislikes === 1) {
      return (
        <h6>
          <strong id="dislikes-count">{props.dislikes} dislike</strong>
        </h6>
      );
    } else {
      return (
        <h6>
          <strong id="dislikes-count">{props.dislikes} dislikes</strong>
        </h6>
      );
    }
  };
  return (
    <>
      <div className="row">
        <Likes />
        <DisLikes />
      </div>
      <Likeanddislikebuttons videoId={props.videoId} />
    </>
  );
}
