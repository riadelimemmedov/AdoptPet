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
import PaymentCancelledCard from './components/PaymentCancelled'
import RegisterCart from './components/Register'


ReactDOM.createRoot(document.getElementById('root')).render(
    <MoralisProvider initializeOnMount={false}>
      <BrowserRouter>
        <Routes>
          <Route exact path="/" element={<App/>}/>
          <Route exact path="cart" element={<Cart/>}/>
          <Route exact path="success" element={<PaymentSuccessCard/>}/>
          <Route exact path="canceled" element={<PaymentCancelledCard/>}/>
          <Route exact path="register" element={<RegisterCart/>}/>
        </Routes>
      </BrowserRouter>
      <ToastContainer />
    </MoralisProvider>
)
