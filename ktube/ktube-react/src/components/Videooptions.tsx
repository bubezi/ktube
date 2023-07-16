function Videooptions () {
    return (
        <>
            <div className="video-options">
                <div className="dropdown">
                    <button className="btn" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="true">
                        <i className="fa-solid fa-ellipsis-vertical"></i>
                    </button>

                    <div className="dropdown-menu dropdown-menu-right" aria-labelledby="dropdownMenuButton"></div>
                </div>
            </div>
        </>
    );
}

export default Videooptions;