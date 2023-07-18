import React from 'react';
import Login from '../Login';

function Auth() {
  const [token, setToken] = React.useState (() => {
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
          <Login saveToken={saveToken} />
        </>
          );
  }else{
    // redirect("http://localhost:5173");
    return(
      <>
        <h1>Already logged in</h1>
      </>
    );
  }
}
export default Auth;
