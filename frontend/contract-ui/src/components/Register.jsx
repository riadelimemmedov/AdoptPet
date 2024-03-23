import React from "react";
import { Navbar } from "./Navbar";

// *SignInCart
const RegisterCart = () => {
    //return jsx to client
    return (
        <>

        <Navbar/>
        <section>
          <div class="w-full lg:w-4/12 px-4 mx-auto pt-6 mt-10">
            <div class="relative flex flex-col min-w-0 break-words w-full mb-6 shadow-lg rounded-lg bg-slate-100 border-0">
              <div class="rounded-t mb-0 px-6 py-6">
                <div class="text-center mb-3">
                  <h6 class="text-blueGray-500 text-sm font-bold">
                    Register with
                  </h6>
                </div>
                <div class="btn-wrapper text-center">
                  <button class="bg-white active:bg-blueGray-50 text-blueGray-700 font-normal px-4 py-2 rounded outline-none focus:outline-none mr-2 mb-1 uppercase shadow hover:shadow-md inline-flex items-center font-bold text-xs ease-linear transition-all duration-150" type="button">
                    <img alt="..." class="w-5 mr-1" src="https://demos.creative-tim.com/notus-js/assets/img/github.svg"/>Github</button>
                  <button class="bg-white active:bg-blueGray-50 text-blueGray-700 font-normal px-4 py-2 rounded outline-none focus:outline-none mr-1 mb-1 uppercase shadow hover:shadow-md inline-flex items-center font-bold text-xs ease-linear transition-all duration-150" type="button">
                    <img alt="..." class="w-5 mr-1" src="https://demos.creative-tim.com/notus-js/assets/img/google.svg"/>Google </button>
                </div>
                <hr class="mt-6 border-b-1 border-blueGray-300"/>
              </div>
              <div class="flex-auto px-4 lg:px-10 py-10 pt-0">
                <div class="text-blueGray-400 text-center mb-3 font-bold">
                  <small>Or register in with credentials</small>
                </div>
                <form>
                    <div class="relative w-full mb-3">
                        <label class="block uppercase text-blueGray-600 text-xs font-bold mb-2" for="grid-password">Username</label>
                        <input type="email" class="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150" placeholder="Username" required={true}/>
                  </div>
                  <div class="relative w-full mb-3">
                    <label class="block uppercase text-blueGray-600 text-xs font-bold mb-2" for="grid-password">Email</label>
                    <input type="email" class="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150" placeholder="Email" required={true}/>
                  </div>
                  <div class="relative w-full mb-3">
                    <label class="block uppercase text-blueGray-600 text-xs font-bold mb-2" for="grid-password">Password</label>
                    <input type="password" class="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150" placeholder="Password" required={true}/>
                  </div>
                  <div class="relative w-full mb-3">
                    <label class="block uppercase text-blueGray-600 text-xs font-bold mb-2" for="grid-password">Repassword</label>
                    <input type="password" class="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150" placeholder="Repassword" required={true}/>
                  </div>
                  <div>
                    <hr className="mb-2 mt-2" />
                    <span>If you have already account? </span>
                    <a href="#" class="font-medium text-blue-600 dark:text-blue-500 hover:underline">Login</a>
                </div>
                  <div class="text-center mt-6">
                    <button class="bg-gray-800 text-white text-sm font-bold uppercase px-6 py-3 rounded shadow hover:shadow-lg outline-none focus:outline-none mr-1 mb-1 w-full ease-linear transition-all duration-150" type="button"> Register </button>
                  </div>
                </form>
              </div>
            </div>
          </div>
          <footer class="relative pt-8 pb-6 mt-2">
            <div class="container mx-auto px-2">
              <div class="flex flex-wrap items-center md:justify-between justify-center">
                <div class="w-full md:w-6/12 px-4 mx-auto text-center">
                  <div class="text-sm text-blueGray-500 font-semibold py-1">
                  </div>
                </div>
              </div>
            </div>
          </footer>
        </section>
        </>
    )
}
export default RegisterCart;
