// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.9;

contract PetAdoption {
    address public owner;
    uint public petIndex = 0;
    uint[] allAdoptedPets;

    mapping(uint => address) public petIdxToOwnerAddress;
    mapping(address => uint[]) public ownerAddressToPetList;

    constructor(uint initialPetIndex) {
        owner = msg.sender;
        petIndex = initialPetIndex;
    }

    function addPet() public {
        require(owner == msg.sender,"Only a contract owner can be add a new pet!");
        petIndex++;
    }

    function adoptPet(uint adoptIdx) public {
        require(adoptIdx < petIndex,"Pet index out of the bounds!");
        require(petIdxToOwnerAddress[adoptIdx] == address(0),"Pet is already adopted!");

        petIdxToOwnerAddress[adoptIdx] = msg.sender;
        ownerAddressToPetList[msg.sender].push(adoptIdx);
        allAdoptedPets.push(adoptIdx);
    }

    function getOwner() public view returns (address) {
        return owner;
    }
}
