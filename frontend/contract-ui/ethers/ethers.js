import { ethers } from 'ethers';

const eth = new ethers.providers.JsonRpcProvider("http://127.0.0.1:8545/")
export default eth
