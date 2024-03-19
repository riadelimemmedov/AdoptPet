import {create} from 'zustand';
import { toast } from 'react-toastify'


// const authNetworkStore = create((set) => {
//     const HARDHAT_NETWORK_ID = Number(import.meta.env.VITE_VUE_HARDHAT_NETWORK_ID); // Replace with your desired network ID
//     // return jsx to client
//     return {
//         isAuthenticated: false,

//         checkAuthentication: async (provider) => {
//             if (typeof provider !== 'undefined') {
//                 await provider.request({ method: 'eth_requestAccounts' });
//                 const isCheck = await this.checkNetwork(provider);
//                 set({ isAuthenticated: isCheck });
//             } else {
//                 toast.error('MetaMask is not installed');
//                 set({ isAuthenticated: false });
//             }
//         },
//         checkNetwork: async (provider) => {
//             console.log("🚀 ~ checkNetwork: ~ provider:", provider)
//             if (provider.net_version !== HARDHAT_NETWORK_ID.toString()) {
//                 if (await this.switchNetwork(provider)) {
//                     return true;
//                 } else {
//                     return false;
//                 }
//             }
//             return true;
//         },
//         switchNetwork: async (provider) => {
//             const chainIdHex = `0x${HARDHAT_NETWORK_ID.toString(16)}`; // Convert to 16-based hexadecimal chainIdHex number
//             try {
//                 await provider.request({
//                     method: 'wallet_switchEthereumChain',
//                     params: [{ chainId: chainIdHex }], // Only accept hex number
//                 });
//                 return true;
//             } catch (error) {
//                 toast.error('Switching to the network failed');
//                 return false;
//             }
//         }
//     };
// });
// export default authNetworkStore

const usePetStore = create((set) => ({
    from_user: "",
    confirmations:null,
    value:"",
    adopted_pet_slug:"",
    payment_options:"",
    setFromUser: (from_user) => set({ from_user: from_user }),
    setConfirmations: (confirmations) => set({ confirmations: confirmations }),
    setValue: (value) => set({ value: value }),
    setAdoptedPetSlug: (adopted_pet_slug) => set({ adopted_pet_slug: adopted_pet_slug }),
    setPaymentOptions: (payment_options) => set({ payment_options: payment_options }),
}))
export default usePetStore
