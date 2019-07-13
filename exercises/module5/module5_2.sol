pragma solidity ^0.5.1;

contract BasicToken {
    mapping(address => uint256) public balaceOf;
    
    constructor(uint initialSupply) public {
        balaceOf[msg.sender] = initialSupply;
    }
    
    function transfer (address _to, uint256 _value) public returns (bool success) {
        require(balaceOf[msg.sender]>=_value);
        require(balaceOf[_to] + _value >=balaceOf[_to]);
        balaceOf[msg.sender] -= _value;
        balaceOf[_to] += _value;
        
        return true;
        
    }
}