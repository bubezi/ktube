import Dropdown from "react-bootstrap/Dropdown";
import { toggleStyle, elipsisStyle } from "../../assets/styles/Styles";
import { useViewerContext } from "../../providers/ViewerProvider";

const Playlistoptions = () => {
  const myToken = useViewerContext().myToken;

  if (myToken) {
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
