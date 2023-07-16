import React, { useState } from 'react';
import PropTypes from 'prop-types';
import { API_URL } from '../constants';
import '../assets/css/Login.css'

async function loginUser(credentials: { username: string, password: string }) {
  return fetch((API_URL+'auth/login/'), {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(credentials)
  })
  .then(data => data.json())
  .then(data => data.token);  // extract token from data
}


interface LoginProps {
  saveToken: React.Dispatch<React.SetStateAction<string | null>>;
}


const Login: React.FC<LoginProps> = ({ saveToken }) => {
  const [username, setUserName] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    // Check for empty fields
    if (!username || !password) {
      alert('Cannot have empty fields');
      return;
    }

    const token = await loginUser({ username, password });
    saveToken(token);
  };

  return (
    <div className="login-wrapper">
      <h1>Please Log In</h1>
      <form onSubmit={handleSubmit}>
        <label>
          <p>Username</p>
          <input type="text" value={username} onChange={e => setUserName(e.target.value)} />
        </label>
        <label>
          <p>Password</p>
          <input type="password" value={password} onChange={e => setPassword(e.target.value)} />
        </label>
        <div>
          <button type="submit">Submit</button>
        </div>
      </form>
    </div>
  );
};

Login.propTypes = {
  saveToken: PropTypes.func.isRequired
};

export default Login;
