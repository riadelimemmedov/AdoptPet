import { useEffect, useState } from 'react';

import { Navbar } from "../components/Navbar";
import { ethers } from "ethers";

import connect_contract from '../../helpers/connect_contract';

// *Cart
export  default function Cart(){
    const [contract,setContract] = useState(null)
    const [provider,setProvider] = useState(window.ethereum)
    const [pets,setPets] = useState()

    // ?initContract
    const initContract = async () => {
        const connected_contract = await connect_contract()
        setContract(connected_contract)
        await getToCart()
    }

    //? getToCart
    const getToCart = async () => {
        if (contract != null){
            const pets = await contract.getCartItems()
            setPets(pets)
        }
    }

    //useEffect
    useEffect(()=>{
        initContract()
    },[])


    //svgStyle
    const svgStyle = {
        width: '50px',
        height: '50px',
    };

    //return jsx to client
    return (
        <>
            <div className="container">
                <div className="navbar-container">
                    <Navbar/>
                </div>
            </div>
            {
                contract != null ? (
                    <div className="grid sm:px-10 lg:grid-cols-2 lg:px-20 xl:px-32 mt-10">
                        <div className="px-4 pt-8">
                            <p className="text-xl font-medium">Order Summary</p>
                            <p className="text-gray-400">Check your items. And select a suitable shipping method.</p>
                            {
                                    pets && pets.length > 0 ? (
                                        pets.map((pet, index) => (
                                            <div key={index} className="mt-8 space-y-3 rounded-lg border bg-white px-2 py-4 sm:px-6">
                                                <div className="flex flex-col rounded-lg bg-white sm:flex-row">
                                                <img className="m-2 h-24 w-28 rounded-md border object-cover object-center" src={pet.photo} alt="" />
                                                <div className="grid grid-cols-1 w-full px-4 py-4">
                                                    <span className="font-semibold">Name:  {pet.name}</span>
                                                    <span className="float-right text-gray-400 p-4 mt-2 mb-2" style={{ backgroundColor: pet.color }}></span>
                                                    <p className="text-lg font-bold">Price: {pet.price.toString()}</p>
                                                </div>
                                                </div>
                                            </div>
                                        ))
                                    ) : (
                                        null
                                    )
                            }
                            <p className="mt-8 text-lg font-medium">Shipping Methods</p>
                            <form className="mt-5 grid gap-6">
                                <div className="relative">
                                <input className="peer hidden" id="radio_1" type="radio" name="radio" checked />
                                <span className="peer-checked:border-gray-700 absolute right-4 top-1/2 box-content block h-3 w-3 -translate-y-1/2 rounded-full border-8 border-gray-300 bg-white"></span>
                                <label className="peer-checked:border-2 peer-checked:border-gray-700 peer-checked:bg-gray-50 flex cursor-pointer select-none rounded-lg border border-gray-300 p-4" for="radio_1">
                                    <img className="w-14 object-contain" src="/images/naorrAeygcJzX0SyNI4Y0.png" alt="" />
                                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512" className="-ml-14" style={svgStyle}>
                                        <path d="M311.9 260.8L160 353.6 8 260.8 160 0l151.9 260.8zM160 383.4L8 290.6 160 512l152-221.4-152 92.8z" />
                                    </svg>
                                    <div className="ml-5 mt-3">
                                    <span className="mt-2 font-semibold">Pay with Ethereum</span>
                                    </div>
                                </label>
                                </div>
                                <div className="relative">
                                <input className="peer hidden" id="radio_2" type="radio" name="radio" checked />
                                <span className="peer-checked:border-gray-700 absolute right-4 top-1/2 box-content block h-3 w-3 -translate-y-1/2 rounded-full border-8 border-gray-300 bg-white"></span>
                                <label className="peer-checked:border-2 peer-checked:border-gray-700 peer-checked:bg-gray-50 flex cursor-pointer select-none rounded-lg border border-gray-300 p-4" for="radio_2">
                                    <img className="w-14 object-contain" src="/images/oG8xsl3xsOkwkMsrLGKM4.png" alt="" />
                                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 512" className="-ml-14" style={svgStyle}>
                                        <path d="M165 144.7l-43.3 9.2-.2 142.4c0 26.3 19.8 43.3 46.1 43.3 14.6 0 25.3-2.7 31.2-5.9v-33.8c-5.7 2.3-33.7 10.5-33.7-15.7V221h33.7v-37.8h-33.7zm89.1 51.6l-2.7-13.1H213v153.2h44.3V233.3c10.5-13.8 28.2-11.1 33.9-9.3v-40.8c-6-2.1-26.7-6-37.1 13.1zm92.3-72.3l-44.6 9.5v36.2l44.6-9.5zM44.9 228.3c0-6.9 5.8-9.6 15.1-9.7 13.5 0 30.7 4.1 44.2 11.4v-41.8c-14.7-5.8-29.4-8.1-44.1-8.1-36 0-60 18.8-60 50.2 0 49.2 67.5 41.2 67.5 62.4 0 8.2-7.1 10.9-17 10.9-14.7 0-33.7-6.1-48.6-14.2v40c16.5 7.1 33.2 10.1 48.5 10.1 36.9 0 62.3-15.8 62.3-47.8 0-52.9-67.9-43.4-67.9-63.4zM640 261.6c0-45.5-22-81.4-64.2-81.4s-67.9 35.9-67.9 81.1c0 53.5 30.3 78.2 73.5 78.2 21.2 0 37.1-4.8 49.2-11.5v-33.4c-12.1 6.1-26 9.8-43.6 9.8-17.3 0-32.5-6.1-34.5-26.9h86.9c.2-2.3 .6-11.6 .6-15.9zm-87.9-16.8c0-20 12.3-28.4 23.4-28.4 10.9 0 22.5 8.4 22.5 28.4zm-112.9-64.6c-17.4 0-28.6 8.2-34.8 13.9l-2.3-11H363v204.8l44.4-9.4 .1-50.2c6.4 4.7 15.9 11.2 31.4 11.2 31.8 0 60.8-23.2 60.8-79.6 .1-51.6-29.3-79.7-60.5-79.7zm-10.6 122.5c-10.4 0-16.6-3.8-20.9-8.4l-.3-66c4.6-5.1 11-8.8 21.2-8.8 16.2 0 27.4 18.2 27.4 41.4 .1 23.9-10.9 41.8-27.4 41.8zm-126.7 33.7h44.6V183.2h-44.6z"/>
                                    </svg>
                                    <div className="ml-5 mt-3">
                                    <span className="mt-2 font-semibold">Pay with Stripe</span>
                                    </div>
                                </label>
                                </div>
                            </form>
                        </div>
                        <div className="mt-10 bg-gray-50 px-4 pt-8 lg:mt-0">
                            <p className="text-xl font-medium">Payment Details</p>
                            <p className="text-gray-400">Complete your order by providing your payment details.</p>
                            <div className="">
                                <label for="email" className="mt-4 mb-2 block text-sm font-medium">Email</label>
                                <div className="relative">
                                    <input type="text" id="email" name="email" className="w-full rounded-md border border-gray-200 px-4 py-3 pl-11 text-sm shadow-sm outline-none focus:z-10 focus:border-blue-500 focus:ring-blue-500" placeholder="your.email@gmail.com" />
                                    <div className="pointer-events-none absolute inset-y-0 left-0 inline-flex items-center px-3">
                                        <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                            <path stroke-linecap="round" stroke-linejoin="round" d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207" />
                                        </svg>
                                    </div>
                                </div>
                                <label for="card-holder" className="mt-4 mb-2 block text-sm font-medium">Card Holder</label>
                                <div className="relative">
                                    <input type="text" id="card-holder" name="card-holder" className="w-full rounded-md border border-gray-200 px-4 py-3 pl-11 text-sm uppercase shadow-sm outline-none focus:z-10 focus:border-blue-500 focus:ring-blue-500" placeholder="Your full name here" />
                                    <div className="pointer-events-none absolute inset-y-0 left-0 inline-flex items-center px-3">
                                        <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                            <path stroke-linecap="round" stroke-linejoin="round" d="M15 9h3.75M15 12h3.75M15 15h3.75M4.5 19.5h15a2.25 2.25 0 002.25-2.25V6.75A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25v10.5A2.25 2.25 0 004.5 19.5zm6-10.125a1.875 1.875 0 11-3.75 0 1.875 1.875 0 013.75 0zm1.294 6.336a6.721 6.721 0 01-3.17.789 6.721 6.721 0 01-3.168-.789 3.376 3.376 0 016.338 0z" />
                                        </svg>
                                    </div>
                                </div>
                                <label for="card-no" className="mt-4 mb-2 block text-sm font-medium">Card Details</label>
                                <div className="flex">
                                    <div className="relative w-7/12 flex-shrink-0">
                                        <input type="text" id="card-no" name="card-no" className="w-full rounded-md border border-gray-200 px-2 py-3 pl-11 text-sm shadow-sm outline-none focus:z-10 focus:border-blue-500 focus:ring-blue-500" placeholder="xxxx-xxxx-xxxx-xxxx" />
                                        <div className="pointer-events-none absolute inset-y-0 left-0 inline-flex items-center px-3">
                                            <svg className="h-4 w-4 text-gray-400" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                                                <path d="M11 5.5a.5.5 0 0 1 .5-.5h2a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1-.5-.5v-1z" />
                                                <path d="M2 2a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2H2zm13 2v5H1V4a1 1 0 0 1 1-1h12a1 1 0 0 1 1 1zm-1 9H2a1 1 0 0 1-1-1v-1h14v1a1 1 0 0 1-1 1z" />
                                            </svg>
                                        </div>
                                    </div>
                                    <input type="text" name="credit-expiry" className="w-full rounded-md border border-gray-200 px-2 py-3 text-sm shadow-sm outline-none focus:z-10 focus:border-blue-500 focus:ring-blue-500" placeholder="MM/YY" />
                                    <input type="text" name="credit-cvc" className="w-1/6 flex-shrink-0 rounded-md border border-gray-200 px-2 py-3 text-sm shadow-sm outline-none focus:z-10 focus:border-blue-500 focus:ring-blue-500" placeholder="CVC" />
                                </div>
                                <label for="billing-address" className="mt-4 mb-2 block text-sm font-medium">Billing Address</label>
                                <div className="flex flex-col sm:flex-row">
                                    <div className="relative flex-shrink-0 sm:w-7/12">
                                        <input type="text" id="billing-address" name="billing-address" className="w-full rounded-md border border-gray-200 px-4 py-3 pl-11 text-sm shadow-sm outline-none focus:z-10 focus:border-blue-500 focus:ring-blue-500" placeholder="Street Address" />
                                        <div className="pointer-events-none absolute inset-y-0 left-0 inline-flex items-center px-3">
                                            <img className="h-4 w-4 object-contain" src="https://flagpack.xyz/_nuxt/4c829b6c0131de7162790d2f897a90fd.svg" alt="" />
                                        </div>
                                    </div>
                                    <select type="text" name="billing-state" className="w-full rounded-md border border-gray-200 px-4 py-3 text-sm shadow-sm outline-none focus:z-10 focus:border-blue-500 focus:ring-blue-500">
                                        <option value="State">State</option>
                                    </select>
                                    <input type="text" name="billing-zip" className="flex-shrink-0 rounded-md border border-gray-200 px-4 py-3 text-sm shadow-sm outline-none sm:w-1/6 focus:z-10 focus:border-blue-500 focus:ring-blue-500" placeholder="ZIP" />
                                </div>
                                <div className="mt-6 border-t border-b py-2">
                                    <div className="flex items-center justify-between">
                                        <p className="text-sm font-medium text-gray-900">Subtotal</p>
                                        <p className="font-semibold text-gray-900">$399.00</p>
                                    </div>
                                    <div className="flex items-center justify-between">
                                        <p className="text-sm font-medium text-gray-900">Shipping</p>
                                        <p className="font-semibold text-gray-900">$8.00</p>
                                    </div>
                                </div>
                                <div className="mt-6 flex items-center justify-between">
                                    <p className="text-sm font-medium text-gray-900">Total</p>
                                    <p className="text-2xl font-semibold text-gray-900">$408.00</p>
                                </div>
                            </div>
                            <button className="mt-4 mb-8 w-full rounded-md bg-gray-900 px-6 py-3 font-medium text-white">Place Order</button>
                        </div>
                    </div>
                    )
                :
                (
                    null
                )
            }
        </>
    );
};
