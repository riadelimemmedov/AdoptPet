//!React
import { useState } from 'react'
import reactLogo from './assets/react.svg'

//!Components
import { PetItem } from './components/Petitem'
import { TxError } from './components/TxError'
import { Navbar } from './components/Navbar'
import { toast } from 'react-toastify'

// HARDHAT_NETWORK_ID
const HARDHAT_NETWORK_ID = Number(import.meta.env.VITE_VUE_HARDHAT_NETWORK_ID)

//*Dapp
function Dapp() {
    const [selectedAddress,setSelectedAddress] = useState(null)

    // ?isAuthenticated
    const isAuthenticated = async () => {
      const provider = window.ethereum
      if (typeof provider !== 'undefined') {
          let accounts = await provider.request({method: "eth_requestAccounts"})
          return true
      } else {
          toast.error("MetaMask is not installed");
          return false
      }
    }

    // ?checkNetwork
    const checkNetwork = async () => {
        if (window.ethereum.networkVersion !== HARDHAT_NETWORK_ID.toString()) {
          if (await switchNetwork()) {
              return true;
          } else {
              return false;
          }
        }
        return true
    }


    // ?switchNetwork
    const switchNetwork = async () => {
        const chainIdHex = `0x${HARDHAT_NETWORK_ID.toString(16)}` //Convert to 16 based hexadecimal chainIdHex number
        if(await isAuthenticated()){
          try {
            await window.ethereum.request({
                method: 'wallet_switchEthereumChain',
                params: [{ chainId: chainIdHex }],//Only accept hex number
            })
            return true
          } catch (error) {
              toast.error("Switching to the network failed")
              return false
            }
        }
        else{
          return false
        }
    }

    // ?initializeDapp
    const initializeDapp = async (address) => {
        if (await isAuthenticated()) {
            setSelectedAddress(address)
            const contract = await initContract()
        }
    }

    // ?initContract
    const initContract = async () => {
      toast.success("I should init the contract !")
    }

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
            <PetItem isAuthenticated={isAuthenticated} checkNetwork={checkNetwork}/>
          </div>
        </div>
        </>
    )
}

export default Dapp
