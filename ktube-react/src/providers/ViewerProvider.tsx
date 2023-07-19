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

interface ViewerProviderProps {
  children: React.ReactNode;
}

const ViewerProvider: React.FC<ViewerProviderProps> = ({ children }) => {
    const [viewer, setViewer] = React.useState(viewerState);
    const [myToken] = React.useState (() => {
        const savedToken = localStorage.getItem('token');
        return savedToken ?? null;
      });

    if (myToken){
        React.useEffect(()=>{
            
            axios({
                method: 'get',
                url: API_URL+'auth/getCurrentViewer',
                headers: {
                    'Authorization': `Token ${myToken}`,
                }
            })
            .then(res=> setViewer(res.data))
            .catch(
                (error)=>{console.log(error)}
            );
        }, []);
        
        return (
            <ViewerContext.Provider value={{ viewer, myToken }}>
                {children}
            </ViewerContext.Provider>
        );
    }else{
        const nullViewer = null;
        const nullMyToken = null;

        return (
            <ViewerContext.Provider value={{ nullViewer, nullMyToken }}>
                {children}
            </ViewerContext.Provider>
        );
    }
};

export const useViewerContext = () => React.useContext(ViewerContext);

export default ViewerProvider;
