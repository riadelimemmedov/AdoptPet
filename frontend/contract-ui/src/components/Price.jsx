// !React
import React from "react"

//!Third party libraries
import useSWR from "swr";



// *PriceCart
const PriceCart = ({price,paymentOption}) => {

    //url endpoint for ethereum pricing converting process
    const root_ethereum_url = `${import.meta.env.VITE_API_ROOT_ENDPOINT_ETHEREUM}`

    // fetcher
    const fetcher = async url => {
        const res = await fetch(url);
        const json = await res.json();
        return json.market_data.current_price.usd ?? null
    }

    //useEthPrice
    const useEthPrice = () => {
        const {data,...rest} = useSWR(
            root_ethereum_url,
            fetcher,
            {refreshInterval:10000}
        )
        return {eth:{data,...rest}}
    }

    // convert
    const convert = () => {
        const {eth} = useEthPrice()
        return eth.data ? (price / eth.data).toFixed(5) : 'Loading'
    }


    //return jsx to client
    return(
        <>
            <hr className="mt-1" />
            {paymentOption === 'ethereum' ? (
                <p className="text-lg font-medium mt-1">
                    <span className="font-medium flex items-center">
                        Price: {convert()}
                        <img className="ml-0 h-5 w-5" src="https://raw.githubusercontent.com/Jerga99/eth-marketplace-course/main/public/small-eth.webp" alt="" />
                    </span>
                    </p>
            ) : paymentOption === 'stripe' ? (
                <p className="text-lg font-medium mt-1"><span className="font-medium">Price: {price}$</span></p>
            ) : (
                null
            )}
        </>
    )
}
export default PriceCart
