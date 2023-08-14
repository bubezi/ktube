import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'

import './index.css'
import "bootstrap";
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap/dist/js/bootstrap.js";

import './assets/css/cdn/cssFamilycookie.css'
import './assets/css/cdn/font-awesome.min.css'
import './assets/css/cdn/free-v4-font-face.min.css'
import './assets/css/cdn/free-v4-shims.min.css'
import './assets/css/cdn/free-v5-font-face.min.css'
import './assets/css/cdn/free.min.css'

import './assets/css/cdn/all.css'

import './assets/css/footer.css'
import './assets/css/home.css'
import './assets/css/main.css'
import './assets/css/profile.css'
import './assets/css/tube.css'
import './assets/css/watch.css'

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
