import Homescreen from "./Homescreen";
import Videos from "./Videos";
import Navbar from "./Navbar";

function Homepage () {
    return (
        <>
            <Navbar username="Bubezi"/>
            <div className="container">
                <Homescreen/>
                <hr />
                <Videos/>
            </div>
        </>
    );           
                      
           
}

export default Homepage;