import { useViewerContext } from "../providers/ViewerProvider";
import Videocard from "./Videocard";
import axios from "axios";
import { API_BASE_URL, API_URL } from "../constants";
import React from "react";
import { VideoType } from "./Videos";
import { PlaylistChannel } from "./Channel";
import Playlistcard from "./Playlistcard";

const Library = () => {
  const myToken = useViewerContext().myToken;
  const [watchlaterVideos, setWatchlaterVideos] = React.useState<VideoType[]>(
    []
  );
  const [savedPlaylists, setSavedPlaylists] = React.useState<PlaylistChannel[]>([]);
  const [myPlaylists, setMyPlaylists] = React.useState<PlaylistChannel[]>([]);

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

    }, [myToken]);

    const Mywatchlater = () => {
      const pluralVideos =
      watchlaterVideos.length === 1 ? "Video" : "Videos";

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
                    <h3>My Watchlater - {watchlaterVideos.length} {pluralVideos}</h3>
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
        return (<Playlistcard key={playlist.id} colSize="4" playlist={playlist}/>);
      });

      return (
      <>
        <div className="row box-element">
          <div className="col-lg-12">
            <div className="row">
              <h3>My Saved Playlists - {savedPlaylists.length} {pluralSavedPlaylists}</h3>
            </div>
          </div>
        </div>
          <div className="row">{showSavedPlaylists}</div>
      </>
      );
    }

    const MyPlaylists = () => {
      const pluralMyPlaylists =
      myPlaylists.length === 1 ? "playlist" : "playlists";

      const showMyPlaylists = myPlaylists.map((playlist) => {
        return (<Playlistcard key={playlist.id} colSize="4" playlist={playlist}/>);
      });

      return (
      <>
        <div className="row box-element">
          <div className="col-lg-12">
            <div className="row">
              <h3>My Playlists - {myPlaylists.length} {pluralMyPlaylists}</h3>
            </div>
          </div>
        </div>
          <div className="row">{showMyPlaylists}</div>
      </>
      );
    }

    return (
      <>
        <div className="container">
          <Mywatchlater />
          <MySavedPlaylists/>
          <MyPlaylists/>
        </div>
      </>
    );
  } else {
    location.assign("/auth/login");
  }
};

export default Library;
