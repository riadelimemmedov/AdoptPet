import eth from '../ethers/ethers.js';

// *getSigner
export const getSigner = (wallet_address) => {
    return eth.getSigner(wallet_address)
}
