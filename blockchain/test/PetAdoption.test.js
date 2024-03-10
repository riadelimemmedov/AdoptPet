/* eslint-disable no-undef */
//!Paclages
const { expect } = require("chai")
const { ethers } = require("hardhat")
const { loadFixture } = require("@nomicfoundation/hardhat-network-helpers")

//*PetAdoption
// eslint-disable-next-line no-undef
describe("PetAdoption", function () {

	async function deployContractFixture() {
		// eslint-disable-next-line no-undef
		const PETS_COUNT = 5
		const ADOPTED_PED_IDX = 0
		const [deployer,account2,account3] = await hre.ethers.getSigners()
		const contract = await (await ethers.getContractFactory("PetAdoption")).deploy(PETS_COUNT)//initialPetIndex

		await contract.connect(account3).adoptPet(ADOPTED_PED_IDX)

		return {
			deployer,
			account2,
			contract,
			petsAddedCount:PETS_COUNT,
			adoptedPetIdx:ADOPTED_PED_IDX
		}
	}

	// eslint-disable-next-line no-undef
	describe("Deployment", async function () {
		it("should set the right owner to smart contract", async function () {
			const {deployer,contract} = await loadFixture(deployContractFixture)
			expect(contract.signer.address).to.equal(deployer.address)
		})
		it("should return the right owner", async function () {
			const {deployer,contract} = await loadFixture(deployContractFixture)
			const contractOwner = await contract.getOwner()
			expect(contractOwner).to.equal(deployer.address)
		})
		it("should have a non-null contract address", async function () {
			const {contract} = await loadFixture(deployContractFixture)
			expect(contract.address).to.not.be.null
		})
	})

	describe("Add Pet",function () {
		it("should revert with the right error in case of other account",async function () {
			const {account2,contract} = await loadFixture(deployContractFixture)
			await expect(contract.connect(account2).addPet()).to.be.revertedWith("Only a contract owner can be add a new pet!")//Error text must be match to require message text on smart contract
		})
		it("should increase pet index", async function () {
			const {petsAddedCount,contract} = await loadFixture(deployContractFixture)
			await contract.addPet()
			expect(await contract.petIndex()).to.equal(petsAddedCount+1)//I am wait 6
		})
	})

	describe("Adopt Pet",function () {
		it("should revert with index out of bounds", async function () {
			const {contract,petsAddedCount} = await loadFixture(deployContractFixture)
			await expect(contract.adoptPet(petsAddedCount)).to.be.revertedWith("Pet index out of the bounds!")
			await expect(contract.adoptPet(-1)).to.be.rejectedWith("value out-of-bounds")
		})
		it("should revert with the pet is already adopted", async function () {
			const {contract,adoptedPetIdx} = await loadFixture(deployContractFixture)
			await expect(contract.adoptPet(adoptedPetIdx)).to.be.revertedWith("Pet is already adopted!")
		})
		it("should adopt pet successfully", async function () {
			const {contract,account2} = await loadFixture(deployContractFixture)
			const firstPetIdx = 1
			const secondPetIdx = 4

			await expect(contract.connect(account2).adoptPet(firstPetIdx)).not.to.be.reverted
			await contract.connect(account2).adoptPet(secondPetIdx)

			const petOwnerAddress = await contract.petIdxToOwnerAddress(firstPetIdx)
			expect(petOwnerAddress).to.be.equal(account2.address)

			const petsByOwner = await contract.connect(account2).getAllAdoptedPetsByOwner()
			const allAdoptedPets = await contract.getAllAdoptedPets()

			expect(petsByOwner.length).to.be.equal(2)
			expect(allAdoptedPets.length).to.be.equal(3)

			expect(await contract.ownerAddressToPetList(account2.address,0)).to.be.equal(firstPetIdx)
			expect(await contract.allAdoptedPets(2)).to.equal(secondPetIdx)

			const zeroAddress = await contract.petIdxToOwnerAddress(85)//If not find address match to petId,return zero address => 0x0000000000000000000000000000000000000000 like this
			expect(zeroAddress).to.be.equal("0x0000000000000000000000000000000000000000")
		})
	})

	describe("Add to cart",function(){
		it("should add to card succsesfully",async function () {
			const {account2,contract} = await loadFixture(deployContractFixture)

			const pet_id = 1
			const pet_name = "Rex"
			const pet_color = "red"
			const pet_price = 100
			const pet_photo = "https://images.unsplash.com/photo-1600682011352-e448301668e7?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1348&q=40"

			expect(account2).not.be.null
			await expect(contract.addToCart(pet_id,pet_name,pet_color,pet_price,pet_photo)).not.to.be.reverted
			expect(contract.getCartItems()).not.be.null
		})
		it("should match added and returned pet",async function(){
			const {account2,contract} = await loadFixture(deployContractFixture)


			const pet_id = 1
			const pet_name = "Rex"
			const pet_color = "red"
			const pet_price = 100
			const pet_photo = "https://images.unsplash.com/photo-1600682011352-e448301668e7?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1348&q=40"

			await expect(contract.connect(account2)).not.to.be.reverted
			await expect(contract.connect(account2).addToCart(pet_id, pet_name, pet_color, pet_price, pet_photo)).not.to.be.reverted

			const cartItems = await contract.connect(account2).getCartItems()
			expect(account2).not.be.null
			expect(cartItems.length).to.be.equal(1)
			expect(cartItems[0].id).to.be.equal(pet_id)
			expect(cartItems[0].name).to.be.equal(pet_name)
			expect(cartItems[0].color).to.be.equal(pet_color)
			expect(cartItems[0].price).to.be.equal(pet_price)
			expect(cartItems[0].photo).to.be.equal(pet_photo)
		})
	})

	describe("Remove the cart",function(){
		it("should remove the cart successfully",async function(){
			const {account2,contract} = await loadFixture(deployContractFixture)

			const pet_id = 1
			const pet_name = "Rex"
			const pet_color = "red"
			const pet_price = 100
			const pet_photo = "https://images.unsplash.com/photo-1600682011352-e448301668e7?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1348&q=40"

			expect(account2).not.be.null
			await expect(contract.addToCart(pet_id,pet_name,pet_color,pet_price,pet_photo)).not.to.be.reverted // 0 index
			await expect(contract.addToCart(pet_id,pet_name,pet_color,pet_price,pet_photo)).not.to.be.reverted // 1 index
			await expect(contract.addToCart(pet_id,pet_name,pet_color,pet_price,pet_photo)).not.to.be.reverted// 2 index
			expect(contract.getCartItems()).not.be.null

			expect(await contract.getCartLength().then(value => parseInt(value.toString()))).equal(3)

			await expect(contract.removeCart(0)).not.to.be.reverted
			await expect(contract.removeCart(5)).to.be.revertedWith("Invalid index")

			expect(await contract.getCartLength().then(value => parseInt(value.toString()))).equal(2)
		})
	})


})
