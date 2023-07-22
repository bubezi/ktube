import Homescreen from "./Homescreen";
import Videos from "./Videos";
import Footer from "./Footer";

function Homepage () {
    document.title="Home | KTUBE";
    return (
        <>
            <div className="container">
                <Homescreen/>
                <hr />
                <Videos/>
            </div>
            <Footer/>
        </>
    );           
                      
           
}

export default Homepage;