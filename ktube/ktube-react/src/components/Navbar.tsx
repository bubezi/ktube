function Navbar (props) {
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
                        </div>
                    </li>
                    </ul>
                </div>
            </div>
        </>
    );
}

export default Navbar;