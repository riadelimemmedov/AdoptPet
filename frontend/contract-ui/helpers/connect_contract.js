// !Contracts
import * as pet_local from '../contracts/PetLocal.json' assert { type: 'json' };

// ! Ethers
import eth from "../ethers/ethers.js";
import { ethers } from 'ethers';


// *connect_contract
const connect_contract = async() => {
    const signer = eth.getSigner()
    const contract = new ethers.Contract(
        pet_local.default.address,
        pet_local.default.abi,
        signer
    );
    return contract
}
export default connect_contract;
