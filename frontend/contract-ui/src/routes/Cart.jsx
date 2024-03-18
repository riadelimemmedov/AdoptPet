// ! React
import { useEffect, useState,useRef,useCallback } from 'react';

//! Component
import { Navbar } from "../components/Navbar";
import PriceCart from '../components/Price';


// !Helpers methods
import connect_contract from '../../helpers/connect_contract';
import {getSigner} from '../../helpers/get_signer';
import getStripePublishableKey from '../../helpers/init_stripe';



// !Third part packages
import { useMoralis } from "react-moralis";
import { gsap } from "gsap";
import { toast } from 'react-toastify'
import { useNavigate } from "react-router-dom";
import validator from 'email-validator';


// *Cart
export default function Cart(){
    const [contract,setContract] = useState(null)
    const [provider,setProvider] = useState(window.ethereum)
    const [pets,setPets] = useState(null)
    const [paymentOption,setPaymentOption] = useState('ethereum')
    const [signer,setSigner] = useState()
    const [reload,setReload] = useState(false)
    const [paymentIsStart,setPaymentIsStart] = useState(false)
    const [email,setEmail] = useState(null)

    //mavigate
    const navigate = useNavigate();

    //reloadEffect
    const reloadEffect = useCallback(() => setReload(!reload),[reload])

    //moralis
    const { web3,account,Moralis,isAuthenticated,user,authenticate } = useMoralis();


    //? showMessage
    const showMessage = (message_text,message_type) => {
        if(message_type == "success"){
            toast.success(message_text)
        }
        else if(message_type == "error"){
            toast.error(message_text)
        }
        else if(message_type == "info"){
            toast.warning(message_text)
        }
    }

    // ?gsap
    const elementRef = useRef(null);

    // ?getCartItems
    const getCartItems = async () => {
        const connected_contract = await connect_contract()
        const signer = getSigner(account)
        const pets = await connected_contract.connect(signer).getCartItems()
        return pets.length > 0 ? (setPets(pets), setContract(connected_contract), setSigner(signer),false) : true;
    }

    // ?handlePaymentOptionChanged
    const handlePaymentOptionChanged = (event) => {
        const selected_option = event.target.value
        setPaymentOption(selected_option)
    }

    //? removeCart
    const removeCart = async (index) => {
        await contract.connect(signer).removeCart(index)
        await removePet()
        if(await getCartItems()){
            setTimeout(()=>navigate("/"),0)
            setPaymentIsStart(true)
        }
    }

    // ?adoptPet
    const adoptPet = async () => {
        const {isValidEmail,isValidPaymentMethod:ethereum} = checkPaymentCredentials(paymentOption,web3)
        const isCheckedPaymentCredentials = isValidEmail && ethereum ? true : false
        if(isCheckedPaymentCredentials){
            setPaymentIsStart(true)
            pets.map(async(pet,index) => {
                await contract.connect(signer).adoptPet(index)
                await removeCart(index >= 1 ? index-1 : 0)
            })
        }
        else{
            setPaymentIsStart(false)
        }
    }

    // ?removePet
    const removePet = async () => {
        const element = elementRef.current;
        if (element) {
            gsap.to(element, {
                opacity: 0,
                height: 0,
                duration: 0.3,
                onComplete: () => {
                    // Remove the element from the DOM
                    element.remove();
                },
            });
        }
    }

    // ?validateEmail
    const validateEmail = () => {
        const isValidEmail = validator.validate(email);
        if(!isValidEmail) {
            showMessage('Invalid email address', 'error')
            return false
        }
        return true
    }

    // ?validatePaymentMethod
    const validatePaymentMethod = (payment_method,wallet_public_key=null) => {
        if(payment_method=='ethereum' && wallet_public_key == web3){
            return web3
        }
        else if(payment_method=='stripe' && wallet_public_key){
            const stripe = getStripePublishableKey()
            return stripe
        }
    }

    //? checkPaymentCredentials
    const checkPaymentCredentials = (payment_method,wallet_public_key=null) => {//ethereum or stripe
        const isValidEmail = validateEmail()
        const isValidPaymentMethod = validatePaymentMethod(payment_method, wallet_public_key)
        if(isValidEmail && isValidPaymentMethod){
            return {isValidEmail,isValidPaymentMethod}
        }
    }

    //?handlePurchase
    const handlePurchase = () =>{
        const {isValidEmail,isValidPaymentMethod:stripe} = checkPaymentCredentials(paymentOption,true)
        const isCheckedPaymentCredentials = isValidEmail && stripe ? true : false
        if(isCheckedPaymentCredentials){
            setPaymentIsStart(true)
            fetch('http://localhost:8000/orders/create-checkout-session', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ book_id: 1 }),
            })
            .then((result) => {
                return result.json()
            })
            .then((data) => {
                setPaymentIsStart(false)
                return stripe.redirectToCheckout({ sessionId: data.sessionId });
            })
            .then((res) => {
                console.log(res);
            });
        }
        else{
            return null
        }

    }

    //useEffect
    useEffect(()=>{
        getCartItems()
    },[account])


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
                contract != null || pets != null ? (
                    <div className="grid sm:px-10 lg:grid-cols-2 lg:px-20 xl:px-32 mt-10">
                        <div className="px-4 pt-8">
                            <p className="text-xl font-medium">Order Summary</p>
                            <p className="text-gray-400">Check your items. And select a suitable shipping method.</p>
                            {
                                    pets && pets.length > 0 ? (
                                        pets.map((pet, index) => (
                                            <div key={index} className="mt-8 space-y-3 rounded-lg border bg-white px-2 py-4 sm:px-6" ref={elementRef}>
                                                <div className="flex flex-col rounded-lg bg-white sm:flex-row">
                                                    <img className="m-2 h-24 mt-5 w-28 rounded-md border object-cover object-center" src={pet.photo} alt="" />
                                                    <div className="grid grid-cols-1 w-full px-4 py-4">
                                                        <span className="font-semibold">Name:  {pet.name}</span>
                                                        <span className="float-right text-gray-400 p-4 mt-2 mb-2" style={{ backgroundColor: pet.color }}></span>
                                                        <PriceCart price={pet.price.toString()} paymentOption={paymentOption}/>
                                                    </div>
                                                </div>
                                                <div className="flex justify-end">
                                                <button onClick={()=>removeCart(index)} stype="button" className="text-white bg-red-500 -mt-12 mr-4 -ml-2 focus:ring-4 focus:outline-none focus:ring-red-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center me-2 dark:bg-red-600 dark:hover:bg-red-800 dark:focus:ring-red-800 inline-flex items-center">
                                                    Remove cart
                                                </button>
                                                </div>
                                            </div>
                                        ))
                                    ) : (
                                        null
                                    )
                            }
                            <p className="mt-8 text-lg font-medium">Shipping Methods</p>
                            <form className="mt-5 grid gap-6">
                                Payment option is --- {paymentOption}
                                <div className="relative">
                                <input className="peer hidden" id="radio_1" type="radio" name="radio" value="ethereum" onChange={handlePaymentOptionChanged} checked={paymentOption === 'ethereum'}/>
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
                                <input className="peer hidden" id="radio_2" type="radio" name="radio" value="stripe" onChange={handlePaymentOptionChanged} checked={paymentOption === 'stripe'}/>
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
                            <p className="text-gray-400">Set your email for security purpose</p>
                            <div className="">
                                <label for="email" className="mt-4 mb-2 block text-sm font-medium">Email</label>
                                <div className="relative">
                                    <input onChange={(e)=>setEmail(e.target.value)} type="text" id="email" name="email" className="w-full rounded-md border border-gray-200 px-4 py-3 pl-11 text-sm shadow-sm outline-none focus:z-10 focus:border-blue-500 focus:ring-blue-500" placeholder="your.email@gmail.com" required/>
                                    <div className="pointer-events-none absolute inset-y-0 left-0 inline-flex items-center px-3">
                                        <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                            <path stroke-linecap="round" stroke-linejoin="round" d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207" />
                                        </svg>
                                    </div>
                                </div>
                            </div>
                            {
                                paymentOption == "ethereum" ? (
                                    <button onClick={() => adoptPet()} className="mt-4 mb-8 w-full rounded-md bg-gray-900 px-6 py-3 font-medium text-white">
                                        {
                                            paymentIsStart ? (
                                                <div>
                                                    <svg aria-hidden="true" role="status" class="inline w-4 h-4 me-3 text-white animate-spin" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
                                                        <path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="#E5E7EB"/>
                                                        <path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentColor"/>
                                                    </svg>
                                                    <span className='mb-1'>Please Wait</span>
                                                </div>
                                            )
                                            :
                                            (
                                                <span>Adopt</span>
                                            )
                                        }
                                    </button>
                                )
                                :
                                (
                                <button onClick={()=>handlePurchase()} className="mt-4 mb-8 w-full rounded-md bg-gray-900 px-6 py-3 font-medium text-white">
                                    {
                                        paymentIsStart ? (
                                            <div>
                                                <svg aria-hidden="true" role="status" class="inline w-4 h-4 me-3 text-white animate-spin" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
                                                    <path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="#E5E7EB"/>
                                                    <path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentColor"/>
                                                </svg>
                                                <span className='mb-1'>Please Wait</span>
                                            </div>
                                        )
                                        :
                                        (
                                            <span>Adopt</span>
                                        )
                                    }
                                </button>
                                )
                            }
                        </div>
                    </div>
                    )
                :
                (
                    <div class="p-10 text-sm text-yellow-800 rounded-lg bg-yellow-50 text-center mt-20 dark:bg-gray-800 dark:text-yellow-300" role="alert">
                        <span class="font-medium text-centers">You don't have have any product on your cart</span>. Please first add pet to cart.
                    </div>
                )
            }
        </>
    );
};
