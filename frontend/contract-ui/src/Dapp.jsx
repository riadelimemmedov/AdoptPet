//!React
import { useState } from 'react'
import reactLogo from './assets/react.svg'

//!Components
import { PetItem } from './components/Petitem'
import { TxError } from './components/TxError'
import { Navbar } from './components/Navbar'

//*Dapp
function Dapp() {
  //return jsx to client
  return (
    <>
      <div className="container">
        {/*<TxError/>*/}
        <br />
        <div className="navbar-container">
          <Navbar/>
        </div>
        <div className="items">
          <PetItem/>
        </div>
      </div>
      </>
  )
}

export default Dapp
