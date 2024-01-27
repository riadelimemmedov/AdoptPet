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
		const [deployer,account2] = await hre.ethers.getSigners()
		const contract = await (await ethers.getContractFactory("PetAdoption")).deploy()
		const randomNumber = Math.random()
		return {
			deployer,
			account2,
			contract,
			randomNumber
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
	})
})