// import React, { useState } from 'react';

// export function DropdownComponent() {
//   const [dropdownOpen, setDropdownOpen] = useState(false);

//   const toggleDropdown = () => {
//     setDropdownOpen(!dropdownOpen);
//   };

//   return (
//     <div className="dropdown">
//       <button
//         className="btn"
//         type="button"
//         onClick={toggleDropdown}
//       >
//         Dropdown
//       </button>
//       {dropdownOpen ? (
//         <div className="dropdown-menu">
//           <a className="dropdown-item" href="#">
//             Item 1
//           </a>
//           <a className="dropdown-item" href="#">
//             Item 2
//           </a>
//           <a className="dropdown-item" href="#">
//             Item 3
//           </a>
//         </div>
//       ) : null}
//     </div>
//   );
// }













///////////////////////////////////////////////////////////////////////////





import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap/dist/js/bootstrap.js';
// import $ from 'jquery';
// import Popper from 'popper.js';


// import React from "react";
import axios from "axios";
import { API_URL } from "../constants";

// import { handleAddToPlaylist } from "../functions/fun";

// function DropdownComponent({ options, selectedOption, handleSelection }) {
//   return (
//     <select value={selectedOption} onChange={handleSelection}>
//       {options.map((option) => (
//         <option key={option.id} value={option.value}>
//           {option.label}
//         </option>
//       ))}
//     </select>
//   );
// }


import React, { useState } from 'react';

export function DropCard() {
  const [dropdown, setDropdown] = useState(false);
  const toggleOpen = () => setDropdown(!dropdown);

  const handleItemClick = (action:string) => {
    console.log(`Performing action: ${action}`);
    // add your action handling logic here
  };

  return (
    <div className="dropdown">
        <button onClick={toggleOpen}>
          Dropdown
        </button>
        <div
          className={`dropdown-menu ${dropdown ? 'show' : ''}`}
          aria-labelledby="dropdownMenuButton"
          >
            <a className="dropdown-item" href="#" onClick={() => handleItemClick('delete')}>
              Delete
            </a>
            <a className="dropdown-item" href="#" onClick={() => handleItemClick('pin')}>
              Pin to your Profile
            </a>
         </div>
     </div>
  );
}


const optionsStyle = {
  display: "block",
};

interface PropOptions {
  videoId: number;
  slug: string;
}

interface PropOption {
  playlistName: string;
  playlistId: number;
  videoId: number;
}

function Option(props: PropOption) {
  const [dropdownOpen, setDropdownOpen] = React.useState(false);

  const itemId: string =
    "playlist-" + props.playlistId + "-video-" + props.videoId;
  return (
    <a
      className="dropdown-item add-btn-link update-cart"
      style={optionsStyle}
      // Remove data-toggle="dropdown"
      // Add onClick handler to toggle dropdownOpen state
      onClick={() => setDropdownOpen(!dropdownOpen)}
      aria-haspopup="true"
      aria-expanded={dropdownOpen} // Use dropdownOpen state here
      id={itemId}
    >
      Add video to {props.playlistName}
    </a>
  );
}

interface Playlist {
  id: number;
  name: string;
}

function Videooptions(props: PropOptions) {

  // // const playlistsInit:Array<Playlist> = [{id: 0, name:''}]
  // // const [playlists, setPlaylists] = React.useState<Array<Playlist>>(playlistsInit);
  const [playlists, setPlaylists] = React.useState<Array<Playlist>>([]);
  const [myToken] = React.useState(() => {
    const savedToken = localStorage.getItem("token");
    return savedToken ?? null;
  });

  const [dropdownOpen, setDropdownOpen] = React.useState(false);
  // Dropdown event handler
  // const toggleDropdown = () => {
  //   setDropdownOpen(!dropdownOpen);
  // };

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
    }, []);

    // React.useEffect(() => {
    //   console.log(playlists);
    // }, [playlists]);

    if (!Array.isArray(playlists)) {
      return null; // or handle the error in an appropriate way
    } else {
      const playlistoptions = playlists.map((playlist) => {
        if (playlist.id !== 0) {
          const playlistName = `${playlist.name}`;
          const playlistId = playlist.id;

          return (
            <Option
              key={playlistId}
              playlistName={playlistName}
              playlistId={playlistId}
              videoId={props.videoId}
            />

      //       <DropdownComponent
      //   options={options} // Replace 'options' with your own array of dropdown options
      //   selectedOption={selectedOption} // Pass in the selected option state if needed
      //   handleSelection={handleSelection} // Pass in your event handler function for handling selected options
      // />
          );
        }
      });

      return (
        <>
          <div className="video-options">
          <div className="dropdown">
          <button
            className="btn"
            type="button"
            id="dropdownMenuButton"
            onClick={() => setDropdownOpen(!dropdownOpen)}
          >
            <i className="fa-solid fa-ellipsis-vertical"></i>
          </button>
          {dropdownOpen ? (
            <div
              className="dropdown-menu dropdown-menu-right"
              aria-labelledby="dropdownMenuButton"
            >
              <div className="row">{playlistoptions}</div>
            </div>
          ) : null}
        </div>

          </div>
        </>
      );
    }
  } else {
    return (
      <>
        <div className="video-options">
          <div className="dropdown">
            <button
              className="btn"
              type="button"
              id="dropdownMenuButton"
              data-toggle="dropdown"
              aria-haspopup="true"
              aria-expanded="true"
            >
              <i className="fa-solid fa-ellipsis-vertical"></i>
            </button>
            <div
              className="dropdown-menu dropdown-menu-right"
              aria-labelledby="dropdownMenuButton"
            >
              <a
                href="/auth/login"
                className="dropdown-item add-btn-link update-cart"
                style={optionsStyle}
              >
                Add to playlist
              </a>
            </div>
          </div>
        </div>
      </>
    );
  }
}

export default Videooptions;
