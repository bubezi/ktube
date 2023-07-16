import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import './App.css';
import Dashboard from './components/Dashboard/Dashboard';
import Login from './components/Login';
import Preferences from './components/Preferences/Preferences';
import Loader from './components/Loader';

function App() {
  const [token, setToken] = React.useState (() => {
    // Try to load the token from local storage
    const savedToken = localStorage.getItem('token');
    return savedToken ?? null;
  });

  const saveToken = (userToken: React.SetStateAction<string | null>) => {
    localStorage.setItem('token', String(userToken));
    setToken(userToken);
  };
  
  if(!token) {
    return (
        <>
          <Loader/>
          <Login saveToken={saveToken} />
        </>
          );
  }

  return (
    <div className="wrapper">
      <Loader/>
      <h1>Application</h1>
      <BrowserRouter>
        <Routes>
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/preferences" element={<Preferences />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}
export default App;
