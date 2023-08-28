import { useViewerContext } from "../providers/ViewerProvider";
import Videocard from "./Videocard";
import axios from "axios";
import { API_BASE_URL, API_URL } from "../constants";
import React from "react";
import { VideoType } from "./Videos";
import { PlaylistChannel } from "./Channel";
import Playlistcard from "./Playlistcard";

// interface VideoView {
//   id: number;
//   video: VideoType;
//   viewer: number;
//   viewer_ip: string;
//   viewed_on: string;
// }

const Library = () => {
  const myToken = useViewerContext().myToken;
  const [watchlaterVideos, setWatchlaterVideos] = React.useState<VideoType[]>(
    []
  );
  const [savedPlaylists, setSavedPlaylists] = React.useState<PlaylistChannel[]>(
    []
  );
  const [myPlaylists, setMyPlaylists] = React.useState<PlaylistChannel[]>([]);
  const [myLikedVideos, setMyLikedVideos] = React.useState<VideoType[]>([]);
  const [myHistory, setMyHistory] = React.useState<VideoType[]>([]);

  if (myToken) {
    document.title = "My Library | KTUBE";

    React.useEffect(() => {
      axios({
        method: "get",
        url: API_URL + "watchlaterVideos",
        headers: {
          Authorization: `Token ${myToken}`,
        },
      })
        .then((res) => {
          if (Array.isArray(res.data.watchlater)) {
            setWatchlaterVideos(res.data.watchlater);
          } else {
            setWatchlaterVideos(Array(res.data.watchlater));
          }
        })
        .catch((error) => {
          console.log(error);
        });

      axios({
        method: "get",
        url: API_URL + "savedPlaylists2API",
        headers: {
          Authorization: `Token ${myToken}`,
        },
      })
        .then((res) => {
          if (Array.isArray(res.data.savedPlaylists)) {
            setSavedPlaylists(res.data.savedPlaylists);
          } else {
            setSavedPlaylists(Array(res.data.savedPlaylists));
          }
        })
        .catch((error) => {
          console.log(error);
        });

      axios({
        method: "get",
        url: API_URL + "myPlaylistsAPI",
        headers: {
          Authorization: `Token ${myToken}`,
        },
      })
        .then((res) => {
          if (Array.isArray(res.data.myPlaylists)) {
            setMyPlaylists(res.data.myPlaylists);
          } else {
            setMyPlaylists(Array(res.data.myPlaylists));
          }
        })
        .catch((error) => {
          console.log(error);
        });

      axios({
        method: "get",
        url: API_URL + "myLikedVideosAPI",
        headers: {
          Authorization: `Token ${myToken}`,
        },
      })
        .then((res) => {
          if (Array.isArray(res.data.MyLikedVideos)) {
            setMyLikedVideos(res.data.MyLikedVideos);
          } else {
            setMyLikedVideos(Array(res.data.MyLikedVideos));
          }
        })
        .catch((error) => {
          console.log(error);
        });

      axios({
        method: "get",
        url: API_URL + "myHistoryAPI",
        headers: {
          Authorization: `Token ${myToken}`,
        },
      })
        .then((res) => {
          if (Array.isArray(res.data.MyHistory)) {
            setMyHistory(res.data.MyHistory);
          } else {
            setMyHistory(Array(res.data.MyHistory));
          }
        })
        .catch((error) => {
          console.log(error);
        });
    }, [myToken]);

    const Mywatchlater = () => {
      const pluralVideos = watchlaterVideos.length === 1 ? "Video" : "Videos";

      const showWatchltervideos = watchlaterVideos.map((video) => {
        return (
          <Videocard
            key={video.id}
            channelId={video.channel}
            colSize="4"
            price={video.price}
            slug={video.slug}
            thumbnail={API_BASE_URL + video.thumbnail}
            title={video.title}
            videoId={video.id}
            views={video.views}
          />
        );
      });

      return (
        <>
          <div className="row box-element">
            <div className="col-lg-12">
              <div className="row">
                <h3>
                  My Watchlater - {watchlaterVideos.length} {pluralVideos}
                </h3>
              </div>
            </div>
          </div>
          <div className="row">{showWatchltervideos}</div>
        </>
      );
    };

    const MySavedPlaylists = () => {
      const pluralSavedPlaylists =
        savedPlaylists.length === 1 ? "playlist" : "playlists";

      const showSavedPlaylists = savedPlaylists.map((playlist) => {
        return (
          <Playlistcard key={playlist.id} colSize="4" playlist={playlist} />
        );
      });

      return (
        <>
          <div className="row box-element">
            <div className="col-lg-12">
              <div className="row">
                <h3>
                  My Saved Playlists - {savedPlaylists.length}{" "}
                  {pluralSavedPlaylists}
                </h3>
              </div>
            </div>
          </div>
          <div className="row">{showSavedPlaylists}</div>
        </>
      );
    };

    const MyPlaylists = () => {
      const pluralMyPlaylists =
        myPlaylists.length === 1 ? "playlist" : "playlists";

      const showMyPlaylists = myPlaylists.map((playlist) => {
        return (
          <Playlistcard key={playlist.id} colSize="4" playlist={playlist} />
        );
      });

      return (
        <>
          <div className="row box-element">
            <div className="col-lg-12">
              <div className="row">
                <h3>
                  My Playlists - {myPlaylists.length} {pluralMyPlaylists}
                </h3>
              </div>
            </div>
          </div>
          <div className="row">{showMyPlaylists}</div>
        </>
      );
    };

    const MyLikedVideos = () => {
      const pluralMyLikedVideos =
        myLikedVideos.length === 1 ? "video" : "videos";

      const showMylikedVideos = myLikedVideos.map((likedVideo) => {
        return (
          <Videocard
            key={likedVideo.id}
            channelId={likedVideo.channel}
            colSize="4"
            price={likedVideo.price}
            slug={likedVideo.slug}
            thumbnail={API_BASE_URL + likedVideo.thumbnail}
            title={likedVideo.title}
            videoId={likedVideo.id}
            views={likedVideo.views}
          />
        );
      });

      return (
        <>
          <div className="row box-element">
            <div className="col-lg-12">
              <div className="row">
                <h3>
                  My Liked Videos - {myLikedVideos.length} {pluralMyLikedVideos}
                </h3>
              </div>
            </div>
          </div>
          <div className="row">{showMylikedVideos}</div>
        </>
      );
    };

    const MyHistory = () => {
      const pluralMyHistory = myHistory.length === 1 ? "video" : "videos";

      const showMyHistory = myHistory.map((video, index) => {
        return (
          <Videocard
            key={index}
            colSize="4"
            channelId={video.channel}
            price={video.price}
            slug={video.slug}
            thumbnail={API_BASE_URL + video.thumbnail}
            title={video.title}
            videoId={video.id}
            views={video.views}
          />
        );
      });

      return (
        <>
          <div className="row box-element">
            <div className="col-lg-12">
              <div className="row">
                <h3>
                  My History - {myHistory.length} {pluralMyHistory}
                </h3>
              </div>
            </div>
          </div>
          <div className="row">{showMyHistory}</div>
        </>
      );
    };

    return (
      <>
        <div className="container">
          <Mywatchlater />
          <MySavedPlaylists />
          <MyPlaylists />
          <MyLikedVideos />
          <MyHistory />
        </div>
      </>
    );
  } else {
    location.assign("/auth/login");
  }
};

export default Library;
