pragma solidity >=0.4.16 <0.6.0;

contract Simple {
    function taker(uint _a, uint _b) public returns (uint) {
        return _a + _b;
    }
}