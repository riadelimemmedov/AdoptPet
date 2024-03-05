import { useEffect, useState } from 'react';
import { ToastContainer, toast } from 'react-toastify';
import InfiniteScroll from 'react-infinite-scroll-component';

//*PetItem
export function PetItem({isAuthenticated,checkNetwork}){
    const [petData,setPetData] = useState([])
    const [hasMore,setHasMore] = useState(true)
    const [page,setPage] = useState(1)

    const PAGE_LIMIT = 5

    const url = import.meta.env.VITE_VUE_APP_URL || "http://127.0.0.1:8000";

    useEffect(() => {
        setTimeout(() => {
            getPetData()
        }, 1500);
    },[page])


    // ?getPetData
    const getPetData = async () => {
        const apiUrl = `${url}/pets/?page=${page}`
        try{
            const response = await fetch(apiUrl,{
                method: "GET",
            })
            const {pet_objects,pet_count} = await response.json()
            let pet_data;
            if (pet_objects != undefined) {
                pet_data = [...petData].concat(pet_objects)
            }
            if(petData.length + PAGE_LIMIT >= pet_count){
                setHasMore(false)
            }
            setPetData(pet_data)
        }
        catch(err){
            console.error('Occur error when want to fetch ', err)
        }
    }


    //? addToCart
    const addToCart = async () => {
        const is_auth = await checkNetwork()
        console.log("Add to carttt  ", is_auth)
        if (is_auth){
            toast.success('Added to cart successfully')
        }
    }

    //return jsx to client
    return (
        <>
            {
                    petData ? (
                            <InfiniteScroll dataLength={petData.length} next={()=>setPage(prevState => prevState+1)} hasMore={hasMore} loader={
                                <div className="flex justify-center items-center h-screen">
                                    <div  className="border-t-4 border-b-4 border-gray-500 rounded-full w-12 h-12 animate-spin"></div>
                                </div>
                                }>
                                <ul className="grid grid-cols-1 xl:grid-cols-4 gap-y-10 gap-x-4 items-start p-6 ml-14 mt-14 justify-center">
                                        {
                                            petData.map((pet,index) => (
                                                <li className="relative flex flex-col sm:flex-row xl:flex-col items-start" key={index}>
                                                    <div className="order-1 sm:ml-6 xl:ml-0">
                                                        <h3 class="mb-1 text-slate-900 font-semibold dark:text-slate-200">
                                                            <span className="mb-1 block text-sm leading-6 text-indigo-500">{pet.name}</span>
                                                        </h3>
                                                        <div className="prose prose-slate prose-sm text-slate-600 dark:prose-dark">
                                                            <p>{pet.description}</p>
                                                        </div>
                                                        <a className="group inline-flex items-center h-9 rounded-full text-sm font-semibold whitespace-nowrap px-3 focus:outline-none focus:ring-2 bg-slate-100 text-slate-700 hover:bg-slate-200 hover:text-slate-900 focus:ring-slate-500 dark:bg-slate-700 dark:text-slate-100 dark:hover:bg-slate-600 dark:hover:text-white dark:focus:ring-slate-500 mt-6" href="https://headlessui.dev">
                                                            Learn more
                                                            <span className="sr-only">, Completely unstyled, fully accessible UI components</span>
                                                            <svg
                                                                className="overflow-visible ml-3 text-slate-300 group-hover:text-slate-400 dark:text-slate-500 dark:group-hover:text-slate-400"
                                                                width="3"
                                                                height="6"
                                                                viewBox="0 0 3 6"
                                                                fill="none"
                                                                stroke="currentColor"
                                                                stroke-width="2"
                                                                stroke-linecap="round"
                                                                stroke-linejoin="round"
                                                            >
                                                                <path d="M0 0L3 3L0 6"></path>
                                                            </svg>
                                                        </a>

                                                        <button onClick={addToCart} className="text-white w-55 bg-blue-700 hover:bg-blue-800 focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800
                                                            ml-2 group inline-flex items-center h-9 rounded-full text-sm font-semibold whitespace-nowrap px-3 pr-6 pl-4 focus:outline-none focus:ring-2 ">
                                                            Add to cart
                                                            <svg
                                                                className="overflow-visible ml-1 -mt-2  text-slate-300 group-hover:text-slate-400 dark:text-slate-500 dark:group-hover:text-slate-400"
                                                                width="3"
                                                                height="5"
                                                                viewBox="0 0 3 6"
                                                                fill="none"
                                                                stroke="currentColor"
                                                                stroke-width="2"
                                                                stroke-linecap="round"
                                                                stroke-linejoin="round"
                                                            >
                                                            <path d="M0 1.5A.5.5 0 0 1 .5 1H2a.5.5 0 0 1 .485.379L2.89 3H14.5a.5.5 0 0 1 .491.592l-1.5 8A.5.5 0 0 1 13 12H4a.5.5 0 0 1-.491-.408L2.01 3.607 1.61 2H.5a.5.5 0 0 1-.5-.5M3.102 4l1.313 7h8.17l1.313-7zM5 12a2 2 0 1 0 0 4 2 2 0 0 0 0-4m7 0a2 2 0 1 0 0 4 2 2 0 0 0 0-4m-7 1a1 1 0 1 1 0 2 1 1 0 0 1 0-2m7 0a1 1 0 1 1 0 2 1 1 0 0 1 0-2"/>

                                                            </svg>

                                                        </button>

                                                    </div>
                                                    {
                                                        pet.pet_photo_link != "" ? (
                                                            <img src={pet.pet_photo_link} alt="arrr" className="mb-6 shadow-md rounded-lg bg-slate-50 w-full sm:w-[17rem] sm:mb-0 xl:mb-6 xl:w-full" width="1216" height="640" />
                                                        )
                                                        :
                                                        (
                                                            <img src={url+pet.pet_photo_url} alt="anoorrr" className="mb-6 shadow-md rounded-lg bg-slate-50 w-full sm:w-[17rem] sm:mb-0 xl:mb-6 xl:w-full" width="1216" height="640" style={{width:"346px",height:"230px"}} />
                                                        )
                                                    }
                                                </li>
                                            ))
                                        }
                            </ul>
                        </InfiniteScroll>
                )
                :
                (
                    null
                )
            }
        </>
    )
}
