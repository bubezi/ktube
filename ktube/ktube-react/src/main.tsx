import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'

import './index.css'

import './assets/css/cdn/all.css'
import './assets/css/cdn/bootstrap.css'
import './assets/css/cdn/bootstrap.min.css'
import './assets/css/cdn/cssFamilycookie.css'
import './assets/css/cdn/font-awesome.min.css'
import './assets/css/cdn/free-v4-font-face.min.css'
import './assets/css/cdn/free-v4-shims.min.css'
import './assets/css/cdn/free-v5-font-face.min.css'
import './assets/css/cdn/free.min.css'

import './src/assets/css/footer.css'
import './src/assets/css/home.css'
import './src/assets/css/main.css'
import './src/assets/css/profile.css'
import './src/assets/css/tube.css'
import './src/assets/css/watch.css'

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
