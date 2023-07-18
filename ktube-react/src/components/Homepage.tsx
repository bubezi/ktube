import Homescreen from "./Homescreen";
import Videos from "./Videos";
import Footer from "./Footer";

function Homepage () {
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