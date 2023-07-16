function Footer () {
    return (
        <>
            <footer className="footer-distributed">
                <div className="footer-left">
                    <h3>K<span>TUBE</span></h3>
                        
                    {/* {% if not user.is_authenticated %} */}
                    <p className="footer-links">
                    <a href="#">Home</a>
                    </p>
                    {/* {% else %} */}
                    <p className="footer-links">
                        <a href="#">Home</a>
                        ·
                        <a href="#">Subscriptions</a>
                        ·
                        <a href="#">Library</a>
                    </p>
                    {/* {% endif %} */}
                        
                    <p className="footer-company-name">K <span>TUBE</span> &copy; 2023</p>

                </div>

                <div className="footer-center">

                    <div>
                    <i className="fa fa-map-marker"></i>
                    <p><span>Nairobi</span> Kenya</p>
                    </div>

                    <div> 
                    <i className="fa fa-phone"></i> 
                    <p>+2547 123 456 789</p> 
                    </div> 

                    <div> 
                    <i className="fa fa-envelope"></i> 
                    <p><a href="#" target="_blank">ktube@gmail.com</a></p> 
                    {/* <p><a href="mailto:ktube@gmail.com" target="_blank">ktube@gmail.com</a></p>   */}
                    </div> 

                </div>

                <div className="footer-right">
                    <p className="footer-company-about">
                    <span>About the company</span>
                        Shows That Are Just You
                    </p>    
                    
                    <div className="footer-icons">
                        <a href="#" target="_blank" className="fab fa-discord"></a>
                        <a href="#" target="_blank" className="fab fa-telegram"></a>
                    </div>
                </div>
            </footer>
        </>
    );
}

export default Footer;