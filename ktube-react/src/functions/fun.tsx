import { API_URL } from "../constants";
import axios from "axios";

export const handleAddToPlaylist = (
  videoId: number,
  playlistId: number,
  myToken: string
) => {
  if (!videoId || !playlistId || !myToken) {
    console.error(
      "Missing required parameters videoId, playlistId, or myToken"
    );
    return;
  }

  const data = {
    video_id: videoId,
    playlist_id: playlistId,
  };

  const config = {
    headers: {
      "Content-Type": "application/json",
      Authorization: `Token ${myToken}`,
    },
  };

  axios
    .post(API_URL + "add_video_to_playlist", data, config)
    .then((response) => {
      console.log(response.data);
    })
    .catch((error) => {
      if (error.response) {
        // The request was made and the server responded with a status code
        // that falls out of the range of 2xx
        console.log(error.response.data);
        console.log(error.response.status);
        console.log(error.response.headers);
      } else if (error.request) {
        // The request was made but no response was received
        console.log(error.request);
      } else {
        // Something happened in setting up the request that triggered an Error
        console.log("Error", error.message);
      }
      console.log(error.config);
    });
};

export const handleRemoveFromPlaylist = (
  videoId: number,
  playlistId: number,
  myToken: string
) => {
  const data = {
    video_id: videoId,
    playlist_id: playlistId,
  };

  const config = {
    headers: {
      "Content-Type": "application/json",
      Authorization: `Token ${myToken}`,
    },
  };

  axios
    .post(API_URL + "remove_video_from_playlist", data, config)
    .then((response) => {
      console.log(response.data);
    })
    .catch((error) => {
      if (error.response) {
        // The request was made and the server responded with a status code
        // that falls out of the range of 2xx
        console.log(error.response.data);
        console.log(error.response.status);
        console.log(error.response.headers);
      } else if (error.request) {
        // The request was made but no response was received
        console.log(error.request);
      } else {
        // Something happened in setting up the request that triggered an Error
        console.log("Error", error.message);
      }
      console.log(error.config);
    });
};

export const handleAddToWatchlater = (videoId: number, myToken: string) => {
  const data = {
    video_id: videoId,
  };

  const config = {
    headers: {
      "Content-Type": "application/json",
      Authorization: `Token ${myToken}`,
    },
  };

  axios
    .post(API_URL + "add_video_to_watchlater", data, config)
    .then((response) => {
      console.log(response.data);
    })
    .catch((error) => {
      if (error.response) {
        // The request was made and the server responded with a status code
        // that falls out of the range of 2xx
        console.log(error.response.data);
        console.log(error.response.status);
        console.log(error.response.headers);
      } else if (error.request) {
        // The request was made but no response was received
        console.log(error.request);
      } else {
        // Something happened in setting up the request that triggered an Error
        console.log("Error", error.message);
      }
      console.log(error.config);
    });
};

export const handleRemoveFromWatchlater = (
  videoId: number,
  myToken: string
) => {
  const data = {
    video_id: videoId,
  };

  const config = {
    headers: {
      "Content-Type": "application/json",
      Authorization: `Token ${myToken}`,
    },
  };

  axios
    .post(API_URL + "remove_video_from_watchlater", data, config)
    .then((response) => {
      console.log(response.data);
    })
    .catch((error) => {
      if (error.response) {
        // The request was made and the server responded with a status code
        // that falls out of the range of 2xx
        console.log(error.response.data);
        console.log(error.response.status);
        console.log(error.response.headers);
      } else if (error.request) {
        // The request was made but no response was received
        console.log(error.request);
      } else {
        // Something happened in setting up the request that triggered an Error
        console.log("Error", error.message);
      }
      console.log(error.config);
    });
};

export const subOrUnsub = (
  url: string,
  channelId: number,
  viewerId: number,
  myToken: string
) => {
  if (!channelId || !viewerId || !myToken || !url) {
    console.error(
      "Missing required parameters channelId, viewerId, or myToken"
    );
    return;
  }

  const data = {
    channel_id: channelId,
    viewer_id: viewerId,
  };

  const config = {
    headers: {
      "Content-Type": "application/json",
      Authorization: `Token ${myToken}`,
    },
  };

  axios
    .post(API_URL + url, data, config)
    .then((response) => {
      console.log(response.data);
    })
    .catch((error) => {
      if (error.response) {
        // The request was made and the server responded with a status code
        // that falls out of the range of 2xx
        console.log(error.response.data);
        console.log(error.response.status);
        console.log(error.response.headers);
      } else if (error.request) {
        // The request was made but no response was received
        console.log(error.request);
      } else {
        // Something happened in setting up the request that triggered an Error
        console.log("Error", error.message);
      }
      console.log(error.config);
    });
};

export const saveOrUnSavePlaylist = (
  url: string,
  playlistId: number,
  viewerId: number,
  myToken: string
) => {
  if (!playlistId || !viewerId || !myToken || !url) {
    console.error(
      "Missing required parameters playlistId, viewerId, or myToken"
    );
    return;
  }

  const data = {
    playlist_id: playlistId,
    viewer_id: viewerId,
  };

  const config = {
    headers: {
      "Content-Type": "application/json",
      Authorization: `Token ${myToken}`,
    },
  };

  axios
    .post(API_URL + url, data, config)
    .then((response) => {
      console.log(response.data);
    })
    .catch((error) => {
      if (error.response) {
        // The request was made and the server responded with a status code
        // that falls out of the range of 2xx
        console.log(error.response.data);
        console.log(error.response.status);
        console.log(error.response.headers);
      } else if (error.request) {
        // The request was made but no response was received
        console.log(error.request);
      } else {
        // Something happened in setting up the request that triggered an Error
        console.log("Error", error.message);
      }
      console.log(error.config);
    });
};

export const likeunlikeOrdislikeUndislike = (
  url: string,
  videoId: number,
  viewerId: number,
  myToken: string
) => {
  if (!videoId || !viewerId || !myToken || !url) {
    console.error(
      "Missing required parameters url, videoId, viewerId, or myToken"
    );
    return;
  }

  const data = {
    video_id: videoId,
    viewer_id: viewerId,
  };

  const config = {
    headers: {
      "Content-Type": "application/json",
      Authorization: `Token ${myToken}`,
    },
  };

  axios
    .post(API_URL + url, data, config)
    .then((response) => {
      console.log(response.data);
    })
    .catch((error) => {
      if (error.response) {
        // The request was made and the server responded with a status code
        // that falls out of the range of 2xx
        console.log(error.response.data);
        console.log(error.response.status);
        console.log(error.response.headers);
      } else if (error.request) {
        // The request was made but no response was received
        console.log(error.request);
      } else {
        // Something happened in setting up the request that triggered an Error
        console.log("Error", error.message);
      }
      console.log(error.config);
    });
};

export const toggleItem = (id: string, toggle: boolean) => {
  let element = document.getElementById(id);
  if (element) element.style.display = toggle ? "block" : "none";
};
