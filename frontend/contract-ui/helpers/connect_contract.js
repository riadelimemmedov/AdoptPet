import { ethers } from "ethers";
import pet_local from '../contracts/PetLocal.json'


// !connect_contract
const connect_contract = async(hardhat_provider) => {
    const signer = hardhat_provider.getSigner()
    const contract = new ethers.Contract(
        pet_local.address,
        pet_local.abi,
        signer
    );
    return contract
}
export default connect_contract;
