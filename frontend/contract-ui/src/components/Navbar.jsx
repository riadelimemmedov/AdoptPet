import { ConnectButton,Logo,Button } from 'web3uikit';
import {Link} from 'react-router-dom'

//*Navbar
export function Navbar(){
    //return jsx to client
    return(
        <>
            <nav className="bg-white border-gray-200 dark:bg-gray-900">
                <div className="max-w-screen flex flex-wrap items-center justify-between mx-auto p-4">
                    <a href="/" className="flex items-center space-x-3 rtl:space-x-reverse">
                        <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTg54kp7Ls5r0xQADKRDYdgZl7trqbByWip-A&usqp=CAU" className="h-8" alt="Flowbite Logo" />
                        <div className="self-center text-2xl font-semibold whitespace-nowrap dark:text-white">Adopt Pet</div>
                    </a>
                    <div className="flex items-center md:order-2 space-x-3 md:space-x-0 rtl:space-x-reverse">
                        <span>
                            <Link to={"/cart"} class="relative text-gray-700 hover:text-gray-600 mr-6" href="/wishlist">
                                <svg class="h-5 w-5 md:inline" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M3 3H5L5.4 5M7 13H17L21 5H5.4M7 13L5.4 5M7 13L4.70711 15.2929C4.07714 15.9229 4.52331 17 5.41421 17H17M17 17C15.8954 17 15 17.8954 15 19C15 20.1046 15.8954 21 17 21C18.1046 21 19 20.1046 19 19C19 17.8954 18.1046 17 17 17ZM9 19C9 20.1046 8.10457 21 7 21C5.89543 21 5 20.1046 5 19C5 17.8954 5.89543 17 7 17C8.10457 17 9 17.8954 9 19Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                                </svg>
                                <span class="absolute top-0 left-0 rounded-full bg-indigo-500 text-white p-1 text-xs"></span>
                            </Link>
                        </span>
                        <button type="button" className="flex text-sm bg-gray-800 rounded-full md:me-0 focus:ring-4 focus:ring-gray-300 dark:focus:ring-gray-600" id="user-menu-button" aria-expanded="false" data-dropdown-toggle="user-dropdown" data-dropdown-placement="bottom">
                            <img className="w-8 h-8 rounded-full" src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQIf4R5qPKHPNMyAqV-FjS_OTBB8pfUV29Phg&usqp=CAU" alt="user photo"/>
                        </button>
                        <span>
                            <ConnectButton/>
                        </span>
                    </div>
                </div>
            </nav>
        </>
    )
}
