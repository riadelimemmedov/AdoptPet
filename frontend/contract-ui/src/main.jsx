import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './Dapp'
import './index.css'

import { MoralisProvider } from "react-moralis"
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { BrowserRouter, Routes, Route } from 'react-router-dom';

import Cart from './routes/Cart'
import PaymentSuccessCard from './components/PaymentSuccsess'


ReactDOM.createRoot(document.getElementById('root')).render(
    <MoralisProvider initializeOnMount={false}>
      <BrowserRouter>
        <Routes>
          <Route exact path="/" element={<App/>}/>
          <Route exact path="cart" element={<Cart/>}/>
          <Route exact path="success" element={<PaymentSuccessCard/>}/>
        </Routes>
      </BrowserRouter>
      <ToastContainer />
    </MoralisProvider>
)
