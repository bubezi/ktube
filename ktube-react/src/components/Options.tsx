import React from "react";
import Dropdown from "react-bootstrap/Dropdown";
import { optionsStyle } from "./styles/Styles";

interface PropOption {
  playlistName: string;
  playlistId: number;
  videoId: number;
  add: boolean;
  itemId: string;
  handleMethod: () => Promise<void>;
}
function Option(props: PropOption) {
    let handleClick = () => {};
  
    if (props.add) {
      handleClick = async () => {
        await props.handleMethod();
      };
    } else {
      handleClick = async () => {
        await props.handleMethod();
      };
    }
    return (
      <Dropdown.Item
        style={optionsStyle}
        id={props.itemId}
        href="#"
        onClick={handleClick}
      >
        {props.playlistName}
      </Dropdown.Item>
    );
  }

export default React.memo(Option);
