// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.7.0 <0.9.0;

contract Hello {
    string public myString;
    
    function store(string memory _myString) public {
         myString = _myString;
    }
    
    function retrieve() public view returns(string memory) {
        return myString;
    }
   
}