import { ConnectButton,Logo,Button } from 'web3uikit';

//*Navbar
export function Navbar(){
    //return jsx to client
    return(
        <>
            <nav className="bg-white border-gray-200 dark:bg-gray-900">
                <div className="max-w-screen-xl flex flex-wrap items-center justify-between mx-auto p-4">
                    <a href="https://flowbite.com/" className="flex items-center space-x-3 rtl:space-x-reverse">
                        <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTg54kp7Ls5r0xQADKRDYdgZl7trqbByWip-A&usqp=CAU" className="h-8" alt="Flowbite Logo" />
                        <span className="self-center text-2xl font-semibold whitespace-nowrap dark:text-white">Adopt Pet</span>
                    </a>
                    <div className="flex items-center md:order-2 space-x-3 md:space-x-0 rtl:space-x-reverse -mr-56">
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
