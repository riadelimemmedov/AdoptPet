import { useEffect, useState } from 'react';
import { ToastContainer, toast } from 'react-toastify';
import InfiniteScroll from 'react-infinite-scroll-component';

//*PetItem
export function PetItem(){
    const [petData,setPetData] = useState([])
    const [hasMore,setHasMore] = useState(true)
    const [page,setPage] = useState(1)

    const PAGE_LIMIT = 2

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
            <div className="max-w-5xl mx-auto mt-20">

                {
                    petData.length > 0 ? (
                            <InfiniteScroll dataLength={petData.length} next={()=>setPage(prevState => prevState+1)} hasMore={hasMore} loader={
                                <div className="flex justify-center items-center h-screen">
                                    <div  className="border-t-4 border-b-4 border-gray-500 rounded-full w-12 h-12 animate-spin"></div>
                                </div>
                            }>
                                <div class="grid grid-cols-5 gap-5">
                                    {
                                        petData.map((pet,index) => (
                                                    <div class="w-full max-w-sm bg-white border border-gray-200 rounded-lg shadow dark:bg-gray-800 dark:border-gray-700" key={index}>
                                                        <a href="#">
                                                        <figure class="max-w-lg">
                                                            <img class="h-screen w-full max-w-full" src={url+pet.pet_photo_url ? null : pet_photo_url} alt="image description"/>
                                                        </figure>
                                                        </a>
                                                        <div class="px-5 pb-5">
                                                        <a href="#">
                                                            <h5 class="text-sm font-semibold tracking-tight text-gray-900 dark:text-white mt-2">{pet.name}</h5>
                                                            <hr />
                                                        </a>
                                                        <div class="flex items-center justify-between mt-2">
                                                            <span class="text-md font-bold text-gray-900 dark:text-white">$599</span>
                                                            <a href="#" class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300  rounded-lg text-sm px-1 py-1 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">Add to cart</a>
                                                            </div>
                                                        </div>
                                                    </div>
                                                    ))
                                                }
                                    </div>
                        </InfiniteScroll>
                    )
                    :
                    (
                        <p>Not founds</p>
                    )
                }

            </div>
        </>
    )
}
