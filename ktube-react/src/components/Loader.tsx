import '../assets/css/loaders/loader0.css';

function Loader () {
    return (
        <>
            <div className="loader" id="loader">
            <span className="loading-text">Loading</span>
            <div className="dot-container">
                <div className="dot dot-1"></div>
                <div className="dot dot-2"></div>
                <div className="dot dot-3"></div>
            </div>
            </div>
        </>
    );
}

export default Loader;