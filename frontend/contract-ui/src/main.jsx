import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './Dapp'
import './index.css'

import { MoralisProvider } from "react-moralis"
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';


ReactDOM.createRoot(document.getElementById('root')).render(
    <MoralisProvider initializeOnMount={false}>
      <App />
      <ToastContainer />
    </MoralisProvider>
)
