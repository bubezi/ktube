import { useViewerContext } from "../providers/ViewerProvider";

const Navbar = () => {
  const viewerProvided = useViewerContext();

  const logOut = () => {
    localStorage.removeItem('token');
    location.reload();
  }


  const AuthLinks = () => {
    if(viewerProvided.myToken){
      return(
      <>
          <li className="nav-item dropdown">
              <a
                className="nav-link dropdown-toggle"
                data-toggle="dropdown"
                role="button"
                aria-haspopup="false"
                aria-expanded="false"
              >
                Library
              </a>
              <div className="dropdown-menu">
                <a className="dropdown-item" href="/library">
                  My Library
                </a>
                <div className="dropdown-divider"></div>

                {/* {% if user.is_authenticated %}
                            {% if many_channels %}
                            <a className="dropdown-item" href="{% url 'my_channels' %}">Your Channels</a>
                            <div className="dropdown-divider"></div>
                            {% else %}
                            {% if no_channel %}
                                    <a className="dropdown-item" href="{% url 'create_channel' %}">Create Channel</a>
                                    <div className="dropdown-divider"></div>
                                {% else %}
                                    <a className="dropdown-item" href="{% url 'channel' nav_channel.id %}">Your Channel</a>
                                    <div className="dropdown-divider"></div>
                                    {% endif %}
                                {% endif %}
                            {% endif %} */}

                <a className="dropdown-item" href="#">
                  My Watchlater
                </a>
                <a className="dropdown-item" href="#">
                  My Liked Videos
                </a>
                <a className="dropdown-item" href="#">
                  My History
                </a>
                <a className="dropdown-item" href="#">
                  My Playlists
                </a>

                {/* {% if user.is_authenticated and not no_channel and not many_channels %}
                            <div className="dropdown-divider"></div>
                            <a className="dropdown-item" href="{% url 'create_playlist' nav_channel.id %}">Create Playlist</a>
                            {% elif not user.is_authenticated %}
                                <div className="dropdown-divider"></div>
                                <a className="dropdown-item" href="{% url 'login' %}">Create Playlist</a>
                                {% elif no_channel %}
                                <div className="dropdown-divider"></div>
                                <a className="dropdown-item" href="{% url 'create_channel' %}">Create Channel to Create Playlist</a>
                        {% endif %} */}
              </div>
            </li>

            <li className="nav-item active">
              <a className="nav-link" href="#">
                Subscriptions<span className="sr-only">(current)</span>
              </a>
            </li>

            {/* {% if user.is_authenticated %} */}
            <li className="nav-item dropdown">
              <a
                className="nav-link dropdown-toggle"
                data-toggle="dropdown"
                role="button"
                aria-haspopup="false"
                aria-expanded="false"
              >
                {viewerProvided.viewer.username}
              </a>
              <div className="dropdown-menu">
                <a className="dropdown-item" href="#">
                  Profile
                </a>
                <a className="dropdown-item" href="#">
                  Deposit
                </a>
                {/* {% if user.is_superuser %} */}
                <a className="dropdown-item" href="#">
                  Admin
                </a>
                {/* {% endif %} */}
                <a className="dropdown-item" href="#">
                  Change Password
                </a>
                <a className="dropdown-item" href="#">
                  Reset Password
                </a>
                <div className="dropdown-divider"></div>
                <a className="dropdown-item" href="#">
                  Log Out
                </a>
              </div>
            </li>
            {/* {% endif %}  */}
      </>
      );
    }else{
      return(
      <>
      <li className="nav-item dropdown">
              <a
                className="nav-link dropdown-toggle"
                data-toggle="dropdown"
                role="button"
                aria-haspopup="false"
                aria-expanded="false"
              >
                Library
              </a>
              <div className="dropdown-menu">
                <a className="dropdown-item" href="/auth/login">
                  My Library
                </a>
                
                <div className="dropdown-divider"></div>

                <a className="dropdown-item" href="/auth/login">
                  My Watchlater
                </a>
                <a className="dropdown-item" href="/auth/login">
                  My Liked Videos
                </a>
                <a className="dropdown-item" href="/auth/login">
                  My History
                </a>
                <a className="dropdown-item" href="/auth/login">
                  My Playlists
                </a>
              </div>
            </li>

            <li className="nav-item active">
              <a className="nav-link" href="/auth/login">
                Subscriptions<span className="sr-only">(current)</span>
              </a>
            </li>
      </>
      );
    }
  }

  const AuthButtons = () => {
    if (viewerProvided.myToken) {
      return (
        <div className="form-inline my-2 my-lg-0">
          <a className="btn btn-warning"
          onClick={logOut}>
            Log Out
          </a>
        </div>
      );
    } else {
      return (
        <div className="form-inline my-2 my-lg-0">
          <a href="/auth/login" className="btn btn-warning">
            Login
          </a>
        </div>
      );
    }
  }

  return (
    <>
      <div className="navbar navbar-expand-lg navbar-dark bg-dark">
        <a className="navbar-brand" href="/">
          <div className="logo">
            K <span>TUBE</span>
          </div>
        </a>

        <button
          className="navbar-toggler"
          type="button"
          data-toggle="collapse"
          data-target="#navbarSupportedContent"
          aria-controls="navbarSupportedContent"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span className="navbar-toggler-icon"></span>
        </button>

        <div className="collapse navbar-collapse" id="navbarSupportedContent">
          <ul className="navbar-nav mr-auto">
            <li className="nav-item active">
              <a className="nav-link" href="/">
                Home <span className="sr-only">(current)</span>
              </a>
            </li>
            
            <AuthLinks/>

          </ul>
          <form className="form-inline" method="POST" action="#">
            {/* {% csrf_token %} */}

            <input
              className="form-control mr-sm-2"
              type="search"
              name="searched"
              placeholder="Search K TUBE"
              aria-label="Search"
              id="search-term"
            />
            <button className="btn btn-outline-success my-2 my-sm-0">
              Search
            </button>
          </form>

          <AuthButtons />
        </div>
      </div>
    </>
  );
}

export default Navbar;
