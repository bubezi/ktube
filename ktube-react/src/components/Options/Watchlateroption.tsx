import React from "react";
import Dropdown from "react-bootstrap/Dropdown";
import { optionsStyle } from "../../assets/styles/Styles";
import { handleAddToWatchlater, handleRemoveFromWatchlater } from "../../functions/fun";

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
    handleClick = () => {
      handleAddToWatchlater(props.videoId, props.myToken);
      setAddTo(false);
      setPrompt("Video Added to Watchlater");
    };
  } else {
    handleClick = () => {
      handleRemoveFromWatchlater(props.videoId, props.myToken);
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

export default React.memo(Watchlateroption);
