import React from "react";
import axios from "axios";
import { API_URL } from "../constants";

interface Viewer {
    id: number,
    username: string,
    phone: number,
    gender: string,
    joined: number,
    wallet: number,
}

const defaultValue: unknown = '';

const ViewerContext = React.createContext(defaultValue);

const viewerState :Viewer = {id:0, username:"", phone:0, gender:"", joined:0, wallet:0};


const ViewerProvider = ({ children }) => {
    const [viewer, setViewer] = React.useState(viewerState);

    React.useEffect(()=>{
        axios.get(API_URL+'auth/getCurrentViewer')
            .then(res=> setViewer(res.data))
            .catch((error)=>{console.log(error)});
    }, []);
    
    return (
        <ViewerContext.Provider value={{ viewer }}>
            {children}
        </ViewerContext.Provider>
    );
};

export const useViewerContext = () => React.useContext(ViewerContext);

export default ViewerProvider;
