import React, { useEffect, useState } from 'react';
import {Link,useLocation} from 'react-router-dom'
import connect_contract from '../../helpers/connect_contract';
import { getSigner } from '../../helpers/get_signer';
import { useMoralis } from "react-moralis";
import { Navbar } from './Navbar';


// *PaymentSuccessCard
const PaymentSuccessCard = () => {
    // Moralis
    const { web3,account } = useMoralis();

    // getPaymentSessionId
    const getPaymentSessionId = () => {
        const queryString = window.location.search;
        const params = new URLSearchParams(queryString);
        return params.get('session_id');
    }

    // removePetsFromCard
    const removePetsFromCard = async () => {
        if(getPaymentSessionId() != null){
            const connected_contract = await connect_contract()
            const signer = getSigner(account)
            const pets = await connected_contract.connect(signer).getCartItems()
            pets.length>0&&pets.forEach(async (pet,index) => {
                await connected_contract.connect(signer).removeCart(index)
            })
        }
        else{
            return null
        }
    }

    useEffect(()=>{
        removePetsFromCard()
    },[])


    //return jsx to client
    return (
        <>
            <Navbar/>
            <div class="bg-white p-6  md:mx-auto justify-center mt-20">
                <svg viewBox="0 0 24 24" class="text-green-600 w-16 h-16 mx-auto my-6">
                    <path fill="currentColor"
                        d="M12,0A12,12,0,1,0,24,12,12.014,12.014,0,0,0,12,0Zm6.927,8.2-6.845,9.289a1.011,1.011,0,0,1-1.43.188L5.764,13.769a1,1,0,1,1,1.25-1.562l4.076,3.261,6.227-8.451A1,1,0,1,1,18.927,8.2Z">
                    </path>
                </svg>
                <div class="text-center">
                    <h3 class="md:text-2xl text-base text-gray-900 font-semibold text-center">Payment Done!</h3>
                    <p class="text-gray-600 my-2">Adopted pets successesfully</p>
                    <div class="py-10 text-center">
                        <Link to={'/'} class="px-12 bg-indigo-600 rounded-full hover:bg-indigo-500 text-white font-semibold py-3">
                            Back To Home
                        </Link>
                    </div>
                </div>
            </div>
        </>
    );
};
export default PaymentSuccessCard;
