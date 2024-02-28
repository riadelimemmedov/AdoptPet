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

                <InfiniteScroll dataLength={petData.length} next={()=>setPage(()=>page+1)} hasMore={hasMore} loader={
                    <div className="flex justify-center items-center h-screen">
                        <div  className="border-t-4 border-b-4 border-gray-500 rounded-full w-12 h-12 animate-spin"></div>
                    </div>
                }>
                        {
                            petData.map((pet,index) => (
                                <div className="grid grid-cols-1 gap-5 text-center mt-4 mb-10" key={index}>
                                    <div className="max-w-md mx-auto bg-white rounded-xl shadow-md overflow-hidden md:max-w-2xl">
                                        <div className="md:flex">
                                            <div className="md:shrink-0">
                                                <img className="h-48 w-full object-fill md:h-full md:w-48" src="https://placedog.net/300/200/11" alt="Modern building architecture"/>
                                            </div>
                                            <div className="p-8">
                                                <div className="grid-rows-4 grid-flow-col gap-4 text-left">
                                                    <span className='font-bold text-gray-500'>Name: </span><span>Frieda</span><br />
                                                    <hr />
                                                    <span className='font-bold text-gray-500'>Age: </span><span> 3</span><br />
                                                    <hr />
                                                    <span className='font-bold text-gray-500'>Breed: </span><span> Scottish Terrier</span><br />
                                                    <hr />
                                                    <span className='font-bold text-gray-500'>Location: </span><span> Lisco,Alabama</span><br />
                                                    <hr />
                                                    <span className='font-bold text-gray-500'>Age: </span><span> 3</span><br />
                                                    <hr />
                                                    <span className='font-bold text-gray-500'>Description: </span><span> Lorem ipsum dolor sit amet consectetur, adipisicing elit. Eaque maiores, veniam velit exercitationem totam quibusdam nam harum facilis accusamus nulla.</span><br />
                                                    <hr />
                                                </div>
                                                <button className="bg-sky-300 mt-4 hover:bg-sky-400 rounded py-2 w-full">Adopt Now</button>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            ))
                        }
                </InfiniteScroll>
            </div>
        </>
    )
}
