import { ToastContainer, toast } from 'react-toastify';

//*PetItem
export function PetItem(){
    //return jsx to client
    const notify = () => toast("Wow so easy!");

    //return jsx to client
    return (
        <>
            <div className="max-w-5xl mx-auto mt-20">
                <div className="grid grid-cols-2 gap-5 text-center mt-4 mb-10">
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
            </div>
        </>
    )
}
