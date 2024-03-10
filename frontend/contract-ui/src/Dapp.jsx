//!React
import { useEffect, useState, useCallback } from 'react'


//!Components
import { PetItem } from './components/Petitem'
import { TxError } from './components/TxError'
import { Navbar } from './components/Navbar'
import { toast } from 'react-toastify'
import pet_local from '../contracts/PetLocal.json'

// !Helpers
import connect_contract from '../helpers/connect_contract';

//! State
// import useMoralisStore from '../state/store'

// !Third part packages
import { useMoralis } from "react-moralis";


// HARDHAT_NETWORK_ID
const HARDHAT_NETWORK_ID = Number(import.meta.env.VITE_VUE_HARDHAT_NETWORK_ID)

//*Dapp
function Dapp() {
    //State values
    const [selectedAddress,setSelectedAddress] = useState(null)
    const [contract,setContract] = useState(null)
    const [provider,setProvider] = useState(window.ethereum)
    const [isAdmin,setIsAdmin] = useState(false)
    const [reload,setReload] = useState(false)
    const [isAuthenticated,setIsAuthenticated] = useState(false)


    //reloadEffect
    const reloadEffect = useCallback(() => setReload(!reload),[reload])


    //moralis
    const { web3,account,Moralis } = useMoralis();

    //? checkWeb3
    const checkWeb3 = () => {
      if(web3 != null) {
        return true
      }
      return false
    }

    //? handleAccountsChanged
    if(checkWeb3()) {
        const handleAccountsChanged = (accounts) => {
          checkIsAdmin()
          reloadEffect()
        };
        Moralis.onAccountChanged(handleAccountsChanged);
    }

    // ?isAuthenticated
    const checkIsAuthenticated = async () => {
      if (typeof provider !== 'undefined') {
          await provider.request({method: "eth_requestAccounts"})
          const is_check = await checkNetwork()
          setIsAuthenticated(is_check)
          return is_check
      } else {
          toast.error("MetaMask is not installed");
          setIsAuthenticated(false)
          return false
      }
    }

    // ? checkIsAdmin
    const checkIsAdmin = () => {
      setIsAdmin(false)
      if(account != null && pet_local.deployer != null && account.toLowerCase() === pet_local.deployer.toLowerCase()){
        setIsAdmin(true)
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
        const connected_contract = await connect_contract()
        setContract(connected_contract)
    }

    //useEffect
    useEffect(()=>{
      initContract()
      checkIsAdmin()
    },[account])


    //return jsx to client
    return (
      <>
        <div className="container">
          {/*<TxError/>*/}
          <br />
          <div className="navbar-container">
            <Navbar checkIsAuthenticated={checkIsAuthenticated} isAuthenticated={isAuthenticated} account={account} isAdmin={isAdmin}/>
          </div>
          <div className="items">
            <PetItem checkIsAuthenticated={checkIsAuthenticated} isAuthenticated={isAuthenticated} contract={contract} account={account} isAdmin={isAdmin}/>
          </div>
        </div>
        </>
    )
}
export default Dapp
