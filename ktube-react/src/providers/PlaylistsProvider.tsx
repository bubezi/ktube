import axios from "axios";
import React from "react";
import { API_URL } from "../constants";

interface Playlist {
  id: number;
  name: string;
  videos: Array<number>;
}

interface Watchlater {
  id: number;
  videos: Array<number>;
}

interface PlaylistProvided {
  playlists: Array<Playlist>;
  watchlater: Array<Watchlater>;
  savedPlaylists: Array<number>;
}

const defaultValue: PlaylistProvided = {
  playlists: [{ id: 0, name: "", videos: [0] }],
  watchlater: [{ id: 0, videos: [] }],
  savedPlaylists: [],
};

const PlaylistContext = React.createContext(defaultValue);

interface PlaylistsProvidedProps {
  children: React.ReactNode;
}

const PlaylistProvider: React.FC<PlaylistsProvidedProps> = ({ children }) => {
  const [playlists, setPlaylists] = React.useState<Array<Playlist>>([]);
  const [watchlater, setWatchlater] = React.useState<Array<Watchlater>>([]);
  const [savedPlaylists, setSavedPlaylists] = React.useState<Array<number>>([]);
  const [myToken] = React.useState(() => {
    const savedToken = localStorage.getItem("token");
    return savedToken ?? null;
  });

  if (myToken) {
    React.useEffect(() => {
      axios({
        method: "get",
        url: API_URL + "playlistsHome",
        headers: {
          Authorization: `Token ${myToken}`,
        },
      })
        .then((res) => {
          if (Array.isArray(res.data.playlists)) {
            setPlaylists(res.data.playlists);
          } else {
            // handle error
          }
        })
        .catch((error) => {
          console.log(error);
        });

      axios({
        method: "get",
        url: API_URL + "watchlater",
        headers: {
          Authorization: `Token ${myToken}`,
        },
      })
        .then((res) => {
          if (Array.isArray(res.data.watchlater)) {
            setWatchlater(res.data.watchlater);
          } else {
            setWatchlater(Array(res.data.watchlater));
          }
        })
        .catch((error) => {
          console.log(error);
        });

      axios({
        method: "get",
        url: API_URL + "savedPlaylistsAPI",
        headers: {
          Authorization: `Token ${myToken}`,
        },
      })
        .then((res) => {
          if (Array.isArray(res.data.savedPlaylists.playlists)) {
            setSavedPlaylists(res.data.savedPlaylists.playlists);
          } else {
            setSavedPlaylists(Array(res.data.savedPlaylists.playlists));
          }
        })
        .catch((error) => {
          console.log(error);
        });
    }, []);

    return (
      <PlaylistContext.Provider
        value={{ playlists, watchlater, savedPlaylists }}
      >
        {children}
      </PlaylistContext.Provider>
    );
  } else {
    return (
      <PlaylistContext.Provider
        value={{ playlists, watchlater, savedPlaylists }}
      >
        {children}
      </PlaylistContext.Provider>
    );
  }
};

export const usePlaylistsContext = () => React.useContext(PlaylistContext);

export default PlaylistProvider;
