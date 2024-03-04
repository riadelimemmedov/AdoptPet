// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.9;

// import "hardhat/console.sol"; //If you want use console.log inside the smart contract you need to install hardhat

contract PetAdoption {
    address public owner;
    uint public petIndex = 0;
    uint[] public allAdoptedPets;

    mapping(uint => address) public petIdxToOwnerAddress;
    mapping(address => uint[]) public ownerAddressToPetList;

    struct Pet {
        uint256 id;
        string name;
        string color;
        uint256 price;
        string photo;
    }
    mapping(address => Pet[]) private cart;

    constructor(uint initialPetIndex) {
        owner = msg.sender;
        petIndex = initialPetIndex;
    }

    function addPet() public {
        require(
            owner == msg.sender,
            "Only a contract owner can be add a new pet!"
        );
        petIndex++;
    }

    function adoptPet(uint adoptIdx) public {
        require(adoptIdx < petIndex, "Pet index out of the bounds!");
        require(
            petIdxToOwnerAddress[adoptIdx] == address(0),
            "Pet is already adopted!"
        );

        petIdxToOwnerAddress[adoptIdx] = msg.sender;
        ownerAddressToPetList[msg.sender].push(adoptIdx);
        allAdoptedPets.push(adoptIdx);
    }

    function getOwner() public view returns (address) {
        return owner;
    }

    function getAllAdoptedPetsByOwner() public view returns (uint[] memory) {
        return ownerAddressToPetList[msg.sender];
    }

    function getAllAdoptedPets() public view returns (uint[] memory) {
        return allAdoptedPets;
    }

    function addToCart(
        uint256 _petId,
        string memory _petName,
        string memory _petColor,
        uint256 _petPrice,
        string memory _petPhoto
    ) public {
        Pet memory newPet = Pet(
            _petId,
            _petName,
            _petColor,
            _petPrice,
            _petPhoto
        );
        cart[msg.sender].push(newPet);
    }

    function getCartItems() public view returns (Pet[] memory) {
        return cart[msg.sender];
    }
}
