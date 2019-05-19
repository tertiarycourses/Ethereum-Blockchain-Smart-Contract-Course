pragma solidity >=0.4.16 <0.6.0;

contract Student {
    
    string public name;
    uint public grade;
    
    function getName() public returns (string memory) {
        return name;
    }
    
    function setName(string memory studentName)  public {
        name = studentName;
    }
    
    function getGrade() public returns (uint) {
        return grade;
    }
    
    function setGrade(uint studentGrade)  public {
        grade = studentGrade;
    }
}