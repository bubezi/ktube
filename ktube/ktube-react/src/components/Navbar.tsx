interface Props {
    username: String;
}

function Navbar (props:Props) {
    return (
        <>
            <div className="navbar navbar-expand-lg navbar-dark bg-dark">
                <a className="navbar-brand" href="#"><div className="logo">K <span>TUBE</span></div></a>

                <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                    <span className="navbar-toggler-icon"></span>
                </button>

                <div className="collapse navbar-collapse" id="navbarSupportedContent">
                    <ul className="navbar-nav mr-auto">
                    <li className="nav-item active">
                        <a className="nav-link" href="#">Home <span className="sr-only">(current)</span></a>
                    </li>

                    <li className="nav-item dropdown">
                        <a className="nav-link dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="false" aria-expanded="false">Library</a>
                        <div className="dropdown-menu">
                            <a className="dropdown-item" href="#">My Library</a>
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

                            <a className="dropdown-item" href="#">My Watchlater</a>
                            <a className="dropdown-item" href="#">My Liked Videos</a>
                            <a className="dropdown-item" href="#">My History</a>
                            <a className="dropdown-item" href="#">My Playlists</a>

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
                        <a className="nav-link" href="#">Subscriptions<span className="sr-only">(current)</span></a>
                    </li>

                    {/* {% if user.is_authenticated %} */}
                    <li className="nav-item dropdown">
                        <a className="nav-link dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="false" aria-expanded="false">{props.username}</a>
                        <div className="dropdown-menu">
                            <a className="dropdown-item" href="#">Profile</a>
                            <a className="dropdown-item" href="#">Deposit</a>
                            {/* {% if user.is_superuser %} */}
                            <a className="dropdown-item" href="#">Admin</a>
                            {/* {% endif %} */}
                            <a className="dropdown-item" href="#">Change Password</a>
                            <a className="dropdown-item" href="#">Reset Password</a>
                            <div className="dropdown-divider"></div>
                            <a className="dropdown-item" href="#">Log Out</a>
                        </div>
                    </li>
                    {/* {% endif %}  */}


                    </ul>
                    <form className="form-inline" method='POST' action="#">

                        {/* {% csrf_token %} */}
                        
                        <input className="form-control mr-sm-2" type="search" name="searched" placeholder="Search K TUBE" aria-label="Search"
                        id='search-term'/>
                        <button className="btn btn-outline-success my-2 my-sm-0">Search</button>
                    </form>


                    <div className="form-inline my-2 my-lg-0">
                        {/* {% if user.is_authenticated %} */}
                        <a href="{% url 'logout' %}"className="btn btn-warning">Log Out</a>
                        {/* {% else %} */}
                        {/* <a href="{% url 'login' %}"className="btn btn-warning">Login</a> */}
                        {/* {% endif %} */}

                    </div>
                </div>
            </div>
        </>
    );
}

export default Navbar;