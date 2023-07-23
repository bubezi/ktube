import React from "react";
import Dropdown from "react-bootstrap/Dropdown";
import { optionsStyle } from "./styles/Styles";
import { handleAddToPlaylist, handleRemoveFromPlaylist } from "../functions/fun";

interface PropOption {
  prompt: string;
  playlistId: number;
  videoId: number;
  add: boolean;
  itemId: string;
  myToken: string;
}
function Playlistoption(props: PropOption) {
  const [prompt, setPrompt] = React.useState(props.prompt);
  const [addTo, setAddTo] = React.useState(props.add);
  let handleClick = () => {};

  if (addTo) {
    handleClick = async () => {
      await handleAddToPlaylist(props.videoId, props.playlistId, props.myToken);
      setAddTo(false);
      setPrompt("Video Added click to Remove");
    };
  } else {
    handleClick = async () => {
      await handleRemoveFromPlaylist(props.videoId, props.playlistId, props.myToken);
      setAddTo(true);
      setPrompt("Video Removed click to Add");
    };
  }
  return (
    <Dropdown.Item
      style={optionsStyle}
      id={props.itemId}
      href="#"
      onClick={handleClick}
    >
      {prompt}
    </Dropdown.Item>
  );
}

export default React.memo(Playlistoption);
