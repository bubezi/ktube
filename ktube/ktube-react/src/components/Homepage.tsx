import Homescreen from "./Homescreen";
import Videos from "./Videos";
import Navbar from "./Navbar";
import Footer from "./Footer";

function Homepage () {
    return (
        <>
            <Navbar username="Bubezi"/>
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