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
		const contract = await (await ethers.getContractFactory("PetAdoption")).deploy(PETS_COUNT)

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
	})
})