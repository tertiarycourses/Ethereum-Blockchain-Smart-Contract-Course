# Topic 1 : Solidity

# Hello World contract demo
// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.7.0 <0.9.0;

contract Hello {  
    uint256 public myNum;
    
    function store(uint256 _myNum) public {
         myNum = _myNum;
    }
    
}

# Store and retrive numbers demo
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

# Store and retrive strings demo
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

#  Contructor demo
// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.7.0 <0.9.0;

contract Storage {
    uint256 myNum;

    constructor() {
         myNum = 5;
    }

    function store(uint256 num) public {
        myNum = num;
    }

    function retrieve() public view returns (uint256){
        return myNum;
    }
}

# Activity: Constructor
// SPDX-License-Identifier: MIT
pragma solidity >=0.7.0 <0.9.0;

contract Hello {
    string myString;
    
    constructor() {
        myString = "Hello";
    }
    function store(string memory _myString) public {
        myString = _myString;
    }
    function retrieve() public view returns(string memory) {
        return myString;     
    }  
}

# Constant 
// SPDX-License-Identifier: MIT
pragma solidity >=0.7.0 <0.9.0;

contract MyContract {
    string public constant myString= "Hello"; 
}

# Data Types
// SPDX-License-Identifier: MIT
pragma solidity >=0.7.0 <0.9.0;

contract MyContract {
    string public myString = "myString";
    bool public myBool = true;
    int public myInt = 1;
    uint public myUint = 1;
    uint8 public mUint8 = 8;
    uint256 public myUint265 = 9999;
        
}

# Enum
// SPDX-License-Identifier: MIT
pragma solidity >=0.7.0 <0.9.0;

contract MyContract {
    enum State {Waiting, Ready, Active}
    State public state;
    
    constructor() {
        state = State.Waiting;
    }
    
    function activate() public {
        state = State.Active;
    }
    
    function isActive() public view returns(bool) {
        return state == State.Active;
    }        
}

# Actitivy: Enum
// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.7.0 <0.9.0;

contract TrafficLight {

    enum TrafficLightState {Red, Green, Orange}
    TrafficLightState public state;

    constructor() {
        state = TrafficLightState.Red;
    }

    function RedLight() public {
        state = TrafficLightState.Red;
    }
    
    function GreenLight() public {
        state = TrafficLightState.Green;
    }
    
    function OrangeLight() public {
        state = TrafficLightState.Orange;
    }
}


# Struct
// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.7.0 <0.9.0;

contract Hello {
    struct Person {
        string name;
        uint8 age;
    }
    
    Person[] public person;
    
    function addPerson(string memory _name, uint8 _age) public {
         person.push(Person(_name,_age));
    }

}

# Activity: Struct
// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.7.0 <0.9.0;

contract Hello {
    struct Person {
        string firstname;
        string lastname;
        uint8 age;
        uint8 height;
    }

    Person[] public person;
    
    function addPerson(string memory _firstname, string memory _lastname, uint8 _age, uint8 _height) public {
         person.push(Person(_firstname,_lastname,_age,_height));
    }

}

# Activity: Count No of People
// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.7.0 <0.9.0;

contract Hello {
    struct Person {
        string firstname;
        string lastname;
        uint8 age;
        uint8 height;
    }

    Person[] public person;
    uint8 public peopleCount;
    
    function addPerson(string memory _firstname, string memory _lastname, uint8 _age, uint8 _height) public {
         person.push(Person(_firstname,_lastname,_age,_height));
         peopleCount += 1;
    }
}

# Mapping
// SPDX-License-Identifier: MIT
pragma solidity >=0.7.0 <0.9.0;

contract Hello {
    
 mapping(string => uint8) public person;
    
 function addPerson(string memory _name, uint8 _age) public {
         person[_name] = _age;
    }
}

# Activity: Mapping
// SPDX-License-Identifier: MIT
pragma solidity >=0.7.0 <0.9.0;

contract MyContract {
    
    struct Person {
        uint8 _id;
        string _firstname;
        string _lastname;
    }

    mapping(uint8 => Person) public people;
    uint8 public peopleCount = 0;
    
    function addPerson(string memory _firstName, string memory _lastName) public {
         people[peopleCount] = Person(peopleCount,_firstName, _lastName);
         peopleCount += 1;
    }
        
}

# Global Variables and Payable
// SPDX-License-Identifier: MIT
pragma solidity >=0.6.6 <0.9.0;

contract FundMe {
   
    mapping(address => uint256) public addrToAmt;
    
    function fund() public payable {
        addrToAmt[msg.sender] += msg.value;
    }

}

# Function Modifier
// SPDX-License-Identifier: MIT
pragma solidity >=0.6.6 <0.9.0;

contract FundMe {

    mapping(address => uint256) public addrToAmt;
    address public owner;

    constructor() {
        owner = msg.sender;
    }

    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    }
    
    function fund() public payable onlyOwner {
        addrToAmt[msg.sender] += msg.value;
    }
}

# Activity Function Modifier
// SPDX-License-Identifier: MIT
pragma solidity >=0.7.0 <0.9.0;

contract MyContract {

    struct Person {
        uint8 _id;
        string _firstname;
        string _lastname;
    }
    
    address public owner;
    
    constructor() {
        owner = msg.sender;
    }
    
    modifier onlyOwner() {
        require(owner == msg.sender);
        _;
    }

    mapping(uint8 => Person) public people;
    uint8 public peopleCount = 0;
    
    function addPerson(string memory _firstName, string memory _lastName) public onlyOwner {
         people[peopleCount] = Person(peopleCount,_firstName, _lastName);
         peopleCount += 1;
    }
        
}

# Transfer Function
// SPDX-License-Identifier: MIT
pragma solidity >=0.6.6 <0.9.0;

contract Token {
    mapping(address => uint256) public balances;
    address payable funder;
     address owner;
    
    constructor(address payable _funder)  {
       funder = _funder;
       owner = msg.sender;
    }
    
    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    }
    
    function buyToken() public payable onlyOwner {
      balances[msg.sender] += 1;
      funder.transfer(msg.value);
    }
        
}

# Activity: Transfer Function
/// SPDX-License-Identifier: MIT
pragma solidity >=0.6.6 <0.9.0;

contract Token  {
    mapping(address => uint256) public balances;
    address payable funder;
    address owner;
    
    constructor(address payable _funder)  {
       funder = _funder;
       owner = msg.sender;
    }
    
    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    }
    
    function buyToken() public payable onlyOwner {
      balances[msg.sender] += 1;
      funder.transfer(msg.value);
    }
    
    function sellToken() public payable {
      balances[msg.sender] -= 1;
      payable(owner).transfer(msg.value);
   }
        
}
    
# Event
// SPDX-License-Identifier: MIT
pragma solidity >=0.6.6 <0.9.0;

contract Token {
    mapping(address => uint256) public balances;
    address payable funder;
     address owner;
    
    event Transaction(
        address _buyer,
        uint256 _amount
    );

    constructor(address payable _funder)  {
       funder = _funder;
       owner = msg.sender;
    }
    
    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    }
    
    function buyToken() public payable onlyOwner {
      balances[msg.sender] += 1;
      funder.transfer(msg.value);
      emit Transaction(msg.sender,1);
    }
        
}

# Activity: Event
// SPDX-License-Identifier: MIT
pragma solidity >=0.6.6 <0.9.0;

contract Token  {
    mapping(address => uint256) public balances;
    address payable funder;
    address owner;
    
    constructor(address payable _funder)  {
       funder = _funder;
       owner = msg.sender;
    }
    
    event Transaction(
        address _buyer,
        uint256 _amount
    );

    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    }
    
    function buyToken() public payable onlyOwner {
      balances[msg.sender] += 1;
      funder.transfer(msg.value);
      emit Purchase(msg.sender,1);
    }
    
    function sellToken() public payable {
      balances[msg.sender] -= 1;
      payable(owner).transfer(msg.value);
      emit Transaction(msg.sender,-1);
   }
        
}


## Inheritance
// SPDX-License-Identifier: MIT
pragma solidity >=0.7.0 <0.9.0;

contract ERC20Token {
    string public name;
    mapping (address => uint256) public balances;
    
    constructor(string memory _name) {
        name = _name;
    }
    
    function mint() public virtual {
        balances[tx.origin] ++;
    }

## A Simple ERC20 Token with Inheritance
contract ERC20Token {
    mapping (address => uint256) public balances;
    
    event Transfer(address _from, address _to, uint256 _value); 
    
    constructor() {
        balances[msg.sender] = 100; 
    }
    
    function mint() public virtual {
        balances[tx.origin] ++;
    }
}
contract MyToken is ERC20Token  {
    string public name;
    string public symbol;
    address[] public owners;
     
   constructor(string memory _symbol)  {
        symbol = _symbol;
    }
    
    function mint() public override(ERC20Token) {
        super.mint();
        owners.push(msg.sender);
    }
    
    function sendCoin(address _receiver, uint _amount) public returns(bool sufficient) {
        if (balances[msg.sender] < _amount) return false;  
        balances[msg.sender] -= _amount;
        balances[_receiver] += _amount;
        
        emit Transfer(msg.sender, _receiver, _amount); 
        return true;
    }
    function getBalance(address _addr) public view returns(uint) { 
        //balance check
        return balances[_addr];  
    }
        
}   


