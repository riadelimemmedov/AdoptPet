// !Third part packages
import { useMoralis } from "react-moralis";

//? Moralis properties
const { web3,account,Moralis } = useMoralis();

// export some needed package to abroad
export default function useMoralisInit (){
    if(web3 != null && account != null && Moralis != null){
        return { web3,account,Moralis };
    }
}
