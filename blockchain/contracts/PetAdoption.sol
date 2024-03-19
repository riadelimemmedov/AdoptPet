// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.9;

contract PetAdoption {
    address public owner;
    uint public petIndex = 0;
    uint[] public allAdoptedPets;

    mapping(uint => address) public petIdxToOwnerAddress;
    mapping(address => uint[]) public ownerAddressToPetList;

    struct Pet {
        uint256 id;
        string slug;
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

    // addPet
    function addPet() public {
        require(
            owner == msg.sender,
            "Only a contract owner can be add a new pet!"
        );
        petIndex++;
    }

    //adoptPet
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

    //getOwner
    function getOwner() public view returns (address) {
        return owner;
    }

    //getAllAdoptedPetsByOwner
    function getAllAdoptedPetsByOwner() public view returns (uint[] memory) {
        return ownerAddressToPetList[msg.sender];
    }

    //getAllAdoptedPets
    function getAllAdoptedPets() public view returns (uint[] memory) {
        return allAdoptedPets;
    }

    //addToCart
    function addToCart(
        uint256 _petId,
        string memory _petSlug,
        string memory _petName,
        string memory _petColor,
        uint256 _petPrice,
        string memory _petPhoto
    ) public {
        Pet memory newPet = Pet(
            _petId,
            _petSlug,
            _petName,
            _petColor,
            _petPrice,
            _petPhoto
        );
        cart[msg.sender].push(newPet);
    }

    //getCartItems
    function getCartItems() public view returns (Pet[] memory) {
        return cart[msg.sender];
    }

    //removeCart
    function removeCart(uint256 index) public {
        require(index < cart[msg.sender].length, "Invalid index");
        cart[msg.sender][index] = cart[msg.sender][cart[msg.sender].length - 1];
        cart[msg.sender].pop();
    }

    //getCartLength
    function getCartLength() public view returns (uint256) {
        return cart[msg.sender].length;
    }
}
