import Dropdown from "react-bootstrap/Dropdown";
import { toggleStyle, elipsisStyle } from "../../assets/styles/Styles";
import { useViewerContext } from "../../providers/ViewerProvider";
import { usePlaylistsContext } from "../../providers/PlaylistsProvider";
import React from "react";
import axios from "axios";
import { API_URL } from "../../constants";
import { colorRed } from "../../assets/styles/WatchStyles";
import { saveOrUnSavePlaylist } from "../../functions/fun";

interface Props {
  playlistId: number;
}

const Playlistoptions: React.FC<Props> = ({ playlistId }) => {
  const savedPlaylists = usePlaylistsContext().savedPlaylists;
  const [owner, setOwner] = React.useState<boolean>(false);
  const [playlistIsSaved, setPlaylistIsSaved] = React.useState(
    savedPlaylists.includes(playlistId)
  );
  const myToken = useViewerContext().myToken;
  const viewerId = useViewerContext().viewer.id;

  React.useEffect(() => {
    if (myToken !== null && playlistId !== 0) {
      axios({
        method: "get",
        url: API_URL + "isPlaylistOwner/" + String(playlistId),
        headers: {
          Authorization: `Token ${myToken}`,
        },
      })
        .then((res) => {
          const channelOwner = res.data?.is_owner;
          setOwner(channelOwner);
        })
        .catch((error) => {
          console.log(error);
        });
    }
  }, [playlistId]);

  React.useEffect(() => {
    setPlaylistIsSaved(savedPlaylists.includes(playlistId));
  }, [savedPlaylists]);

  if (myToken) {
    const savePlaylist = () => {
      saveOrUnSavePlaylist(
        "savePlaylistsAPI",
        playlistId,
        viewerId,
        myToken
      );
      setPlaylistIsSaved(true);
    };

    const unSavePlaylist = () => {
      saveOrUnSavePlaylist(
        "unSavePlaylistsAPI",
        playlistId,
        viewerId,
        myToken
      );
      setPlaylistIsSaved(false);
    };
    const DeletePlaylist = () => {
      if (owner) {
        return (
          <Dropdown.Item href="/auth/login" style={colorRed}>
            Delete Playlist
          </Dropdown.Item>
        );
      } else {
        return <></>;
      }
    };
    const SaveOrUnSavePlaylist = () => {
      if (playlistIsSaved) {
        return (
          <Dropdown.Item onClick={unSavePlaylist}>
            Unsave playlist
          </Dropdown.Item>
        );
      } else {
        return (
          <Dropdown.Item onClick={savePlaylist}>
            Save playlist
          </Dropdown.Item>
        );
      }
    };
    return (
      <>
        <div className="video-options">
          <div className="dropdown">
            <Dropdown>
              <Dropdown.Toggle
                id="dropdownMenuButton"
                className="custom-dropdown"
                style={toggleStyle}
              >
                <i
                  className="fa-solid fa-ellipsis-vertical"
                  style={elipsisStyle}
                ></i>
              </Dropdown.Toggle>

              <Dropdown.Menu>
                <SaveOrUnSavePlaylist />
                <DeletePlaylist />
              </Dropdown.Menu>
            </Dropdown>
          </div>
        </div>
      </>
    );
  } else {
    return (
      <>
        <div className="video-options">
          <div className="dropdown">
            <Dropdown>
              <Dropdown.Toggle
                id="dropdownMenuButton"
                className="custom-dropdown"
                style={toggleStyle}
              >
                <i
                  className="fa-solid fa-ellipsis-vertical"
                  style={elipsisStyle}
                ></i>
              </Dropdown.Toggle>

              <Dropdown.Menu>
                <Dropdown.Item href="/auth/login">save playlist</Dropdown.Item>
              </Dropdown.Menu>
            </Dropdown>
          </div>
        </div>
      </>
    );
  }
};

export default Playlistoptions;
