// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.7.0 <0.9.0;

contract Hello {
    uint256 public myNum;
    
    function store(uint256 _myNum) public {
         myNum = _myNum;
    }
    
    function retrieve() public view returns(uint256) {
        return myNum;
    }
   
}