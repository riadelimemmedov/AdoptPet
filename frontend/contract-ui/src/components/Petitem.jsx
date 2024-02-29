import { useEffect, useState } from 'react';
import { ToastContainer, toast } from 'react-toastify';
import InfiniteScroll from 'react-infinite-scroll-component';

//*PetItem
export function PetItem(){
    const [petData,setPetData] = useState([])
    const [hasMore,setHasMore] = useState(true)
    const [page,setPage] = useState(1)

    const PAGE_LIMIT = 5

    const url = "http://127.0.0.1:8000"

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
                                                    <div class="order-1 sm:ml-6 xl:ml-0">
                                                        <h3 class="mb-1 text-slate-900 font-semibold dark:text-slate-200">
                                                            <span class="mb-1 block text-sm leading-6 text-indigo-500">Headless UI</span>
                                                            Completely unstyled, fully accessible UI components
                                                        </h3>
                                                        <div class="prose prose-slate prose-sm text-slate-600 dark:prose-dark">
                                                            <p>Completely unstyled, fully accessible UI components, designed to integrate beautifully with Tailwind CSS.</p>
                                                        </div>
                                                        <a class="group inline-flex items-center h-9 rounded-full text-sm font-semibold whitespace-nowrap px-3 focus:outline-none focus:ring-2 bg-slate-100 text-slate-700 hover:bg-slate-200 hover:text-slate-900 focus:ring-slate-500 dark:bg-slate-700 dark:text-slate-100 dark:hover:bg-slate-600 dark:hover:text-white dark:focus:ring-slate-500 mt-6" href="https://headlessui.dev">
                                                            Learn more
                                                            <span class="sr-only">, Completely unstyled, fully accessible UI components</span>
                                                            <svg
                                                                class="overflow-visible ml-3 text-slate-300 group-hover:text-slate-400 dark:text-slate-500 dark:group-hover:text-slate-400"
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
                                                    </div>
                                                    {
                                                        pet.pet_photo_link != "" ? (
                                                            <img src={pet.pet_photo_link} alt="arrr" class="mb-6 shadow-md rounded-lg bg-slate-50 w-full sm:w-[17rem] sm:mb-0 xl:mb-6 xl:w-full" width="1216" height="640" />
                                                        )
                                                        :
                                                        (
                                                            <img src={url+pet.pet_photo_url} alt="anoorrr" class="mb-6 shadow-md rounded-lg bg-slate-50 w-full sm:w-[17rem] sm:mb-0 xl:mb-6 xl:w-full" width="1216" height="640" style={{width:"346px",height:"230px"}} />
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
                    <p>dsadad</p>
                )
            }
        </>
    )
}
