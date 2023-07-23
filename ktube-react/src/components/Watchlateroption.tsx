import React from "react";
import Dropdown from "react-bootstrap/Dropdown";
import { optionsStyle } from "./styles/Styles";
import { handleAddToWatchlater, handleRemoveFromWatchlater } from "../functions/fun";

interface PropOption {
  prompt: string;
  videoId: number;
  add: boolean;
  itemId: string;
  myToken: string;
}
function Watchlateroption(props: PropOption) {
  const [prompt, setPrompt] = React.useState(props.prompt);
  const [addTo, setAddTo] = React.useState(props.add);
  let handleClick = () => {};

  if (addTo) {
    handleClick = async () => {
      await handleAddToWatchlater(props.videoId, props.myToken);
      setAddTo(false);
      setPrompt("Video Added");
    };
  } else {
    handleClick = async () => {
      await handleRemoveFromWatchlater(props.videoId, props.myToken);
      setAddTo(true);
      setPrompt("Video Removed");
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

export default React.memo(Watchlateroption);
