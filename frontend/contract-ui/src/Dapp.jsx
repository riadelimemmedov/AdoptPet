//!React
import { useEffect, useState } from 'react'
import { ethers } from "ethers";


//!Components
import { PetItem } from './components/Petitem'
import { TxError } from './components/TxError'
import { Navbar } from './components/Navbar'
import { toast } from 'react-toastify'


// !Helpers
import connect_contract from '../helpers/connect_contract';

// HARDHAT_NETWORK_ID
const HARDHAT_NETWORK_ID = Number(import.meta.env.VITE_VUE_HARDHAT_NETWORK_ID)

//*Dapp
function Dapp() {
    const [selectedAddress,setSelectedAddress] = useState(null)
    const [contract,setContract] = useState(null)
    const [provider,setProvider] = useState(window.ethereum)

    // ?isAuthenticated
    const isAuthenticated = async () => {
      if (typeof provider !== 'undefined') {
          await provider.request({method: "eth_requestAccounts"})
          const is_check = await checkNetwork()
          return is_check
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

    // ?initContract
    const initContract = async () => {
        const hardhat_provider = new ethers.providers.Web3Provider(provider)
        const connected_contract = await connect_contract(hardhat_provider)
        setContract(connected_contract)
    }


    //useEffect
    useEffect(()=>{
      initContract()
    },[])

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
            <PetItem isAuthenticated={isAuthenticated} contract={contract}/>
          </div>
        </div>
        </>
    )
}

export default Dapp
