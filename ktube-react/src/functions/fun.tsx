import { API_URL } from "../constants";
import axios from "axios";

export const handleAddToPlaylist = (
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
      .post(API_URL + "add_video_to_playlist", data, config)
      .then((response) => {
        console.log(response.data);
      })
      .catch((error) => {
        console.log(error);
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
        console.log(error);
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
        console.log(error);
      });
  };
  
  export const handleRemoveFromWatchlater = (videoId: number, myToken: string) => {
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
        console.log(error);
      });
  };