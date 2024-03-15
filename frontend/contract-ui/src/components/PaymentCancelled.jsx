import React from "react"
import {Link} from 'react-router-dom'


// *PaymentCancelledCard
const PaymentCancelledCard = () => {
    //return jsx to client
    return (
        <>
            <div className="container mx-auto mt-20">
                <div className="flex justify-center">
                    <div className="w-10/12">
                        <h1 className="text-4xl font-bold mb-4">Your payment was cancelled.</h1>
                        <hr className="my-4" />
                        <br />
                        <Link to={"/"} className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-full text-sm">Back Home</Link>
                    </div>
                </div>
            </div>
        </>
    )
}
export default PaymentCancelledCard;
