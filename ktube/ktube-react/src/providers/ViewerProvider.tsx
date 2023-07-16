import React, { Component } from "react";

const ViewerContext = React.createContext();

const Viewer = {id:0, username:"", phone:0, gender:"", joined:0, wallet:0};

const ViewerProvider = ({ children }) => {
    const [viewer, setViewer] = React.useState(Viewer);
    
    return (
        <ViewerContext.Provider value={{ viewer, setViewer }}>
            {children}
        </ViewerContext.Provider>
    );
};

export const useViewerContext = () => React.useContext(ViewerContext);

export default ViewerProvider;
