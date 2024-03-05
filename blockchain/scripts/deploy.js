/* eslint-disable no-undef */
const hre = require("hardhat")
const fs = require("fs")

// !main
async function main(){
	console.log("Deployment started...")

	const [deployer] = await hre.ethers.getSigners()
	const address = await deployer.getAddress()

	console.log(`Deploying the contract with the account ${address}`)

	const PETS_COUNT = 5
	const PetAdoption = await hre.ethers.getContractFactory("PetAdoption")
	const contract = await PetAdoption.deploy(PETS_COUNT)

	//Get sender user addresss,well you know who deploy that is contract
	const receipt = await contract.deployTransaction.wait()// Line of code is waiting for the deployment transaction to be included in six blocks on the Ethereum blockchain. This is done to ensure that the transaction has sufficient confirmations, which helps to ensure the transaction will not be reversed.

	// Set essential contract information to json file
	await setDeployContract(contract.interface.format("json"),contract.address,hre.network.name,receipt.from)
}

// ?call the main function and check contract is successfully deployed or not
main().catch(error => {
	console.error(error)
	process.exitCode = 1
})


//!setDeployContract
async function setDeployContract(abi,address,network,receipt) {
	const contractData = {abi,address,"network":hre.network.name,"deployer":receipt}
	if(network == "localhost"){
		const filePath = "../frontend/contract-ui/contracts/PetLocal.json"
		fs.writeFileSync(filePath,JSON.stringify(contractData))
		console.log("Our contract deployed --- LOCALHOST ---")
	}
	else{
		const filePath = "../frontend/contract-ui/contracts/PetProd.json"
		fs.writeFileSync(filePath,JSON.stringify(contractData))
		console.log("Our contract deployed --- PROD ---")
	}
}
