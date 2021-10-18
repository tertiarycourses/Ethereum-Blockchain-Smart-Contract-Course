# Topic 3: Deployment

# Compile and Deploy contract on Ganache with Python
import json
from web3 import Web3
from solcx import compile_standard, install_solc

# We add these two lines that we forgot from the video!
print("Installing...")
install_solc("0.8.9")

# Set up web3 connection with Ganache
ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))
chain_id = 1337

# Set a default account to sign transaction
my_address = "0x0fca61a0173FaAec7A64D39c20a1397b361B36B9"
private_key = '4fa754ce854e8e902916b961df6bcca50dd717875843b2e00f65dd3cfd492ba0'

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

# Solidity source code
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.8.9",
)
 
# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["Hello"]["evm"]["bytecode"]["object"]

# get abi
abi = json.loads(compiled_sol["contracts"]["SimpleStorage.sol"]["Hello"]["metadata"])["output"]["abi"]

# Initialize contract
contract = web3.eth.contract(abi=abi, bytecode=bytecode)

# Get the latest transaction
nonce = web3.eth.getTransactionCount(my_address)

# Store value 
transaction = contract.constructor().buildTransaction(
    {"chainId": chain_id, "from": my_address, "nonce": nonce}
)

# Sign the contract transaction
signed_txn = web3.eth.account.sign_transaction(transaction, private_key=private_key)
print("Deploying Contract!")

# Send the contract transaction
tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
print(f"Done! Contract deployed to {tx_receipt.contractAddress}")  

# Test Working with deployed Contracts with Web3

# Access the deployed contract 
contract = web3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

# Step 1: Create the transaction
store_transaction = contract.functions.store("Good Afternoon").buildTransaction(
  {"chainId": chain_id, "from": my_address, "nonce": nonce + 1})

# Step 2: Sign the transaction
signed_txn = web3.eth.account.sign_transaction(store_transaction, private_key=private_key)

# Step 3: Send the transaction
tx_greeting_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = web3.eth.wait_for_transaction_receipt(tx_greeting_hash)

# Retrieve the store value
print(f'The store value is {contract.functions.retrieve().call()}')

# Activity: Compile and Deploy Contract to Rinkeby testnet

import json
from web3 import Web3
from solcx import compile_standard, install_solc
import os

# We add these two lines that we forgot from the video!
print("Installing...")
install_solc("0.8.9")

# Set up web3 connection with Rinkeby
rinkeby_url = "https://rinkeby-light.eth.linkpool.io/"
web3 = Web3(Web3.HTTPProvider(rinkeby_url))
chain_id = 4

# Get your public address and private key from Metamask
my_address = "XXX"
private_key = 'XXXX'

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

# Solidity source code
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.8.9",
)
 
# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["Hello"]["evm"]["bytecode"]["object"]

# get abi
abi = json.loads(compiled_sol["contracts"]["SimpleStorage.sol"]["Hello"]["metadata"])["output"]["abi"]

# Initialize contract
contract = web3.eth.contract(abi=abi, bytecode=bytecode)

# Get the latest transaction
nonce = web3.eth.getTransactionCount(my_address)

# Step 1: Create  the transaction
transaction = contract.constructor().buildTransaction(
    {"chainId": chain_id, "from": my_address, "nonce": nonce})

# Step 2: Sign the transaction
signed_txn = web3.eth.account.sign_transaction(transaction, private_key=private_key)

# Step 3: Send the transaction
tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
print(f"Done! Contract deployed to {tx_receipt.contractAddress}")   

# Working with deployed Contracts
contract = web3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

## Create the transaction
tx_hash = contract.functions.store("Good Afternoon").buildTransaction(
    {"chainId": chain_id, "from": my_address, "nonce": nonce + 1})

## Signed the transaction
signed_txn = web3.eth.account.sign_transaction(tx_hash, private_key=private_key)

## Send the transaction
tx_greeting_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = web3.eth.wait_for_transaction_receipt(tx_greeting_hash)
print(f"Done! Contract deployed to {tx_receipt.contractAddress}")   

## Retrieve the store value
print(contract.functions.retrieve().call())


# Hello Coin
### Solidity #### 
// SPDX-License-Identifier: MIT
pragma solidity >=0.7.0 <0.9.0;
  
contract HelloCoin {
    string public name = 'HelloCoin'; 
    string public symbol = 'hc'; 
    
    mapping (address => uint) balances; 
    
    event Transfer(address _from, address _to, uint256 _value); 
    
    constructor() { 
        balances[msg.sender] = 100; 
        
    }
    
    function mint() public virtual {
        balances[tx.origin] ++;
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

### Web3 #### 
import json
from web3 import Web3

# Set up web3 connection with Ganache
ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

abi = json.loads('[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"_from","type":"address"},{"indexed":false,"internalType":"address","name":"_to","type":"address"},{"indexed":false,"internalType":"uint256","name":"_value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[{"internalType":"address","name":"_addr","type":"address"}],"name":"getBalance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"mint","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_receiver","type":"address"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"sendCoin","outputs":[{"internalType":"bool","name":"sufficient","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"}]')
bytecode = "0x60806040526040518060400160405280600981526020017f48656c6c6f436f696e00000000000000000000000000000000000000000000008152506000908051906020019061004f9291906100f4565b506040518060400160405280600281526020017f68630000000000000000000000000000000000000000000000000000000000008152506001908051906020019061009b9291906100f4565b503480156100a857600080fd5b50612710600260003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020819055506101f8565b82805461010090610197565b90600052602060002090601f0160209004810192826101225760008555610169565b82601f1061013b57805160ff1916838001178555610169565b82800160010185558215610169579182015b8281111561016857825182559160200191906001019061014d565b5b509050610176919061017a565b5090565b5b8082111561019357600081600090555060010161017b565b5090565b600060028204905060018216806101af57607f821691505b602082108114156101c3576101c26101c9565b5b50919050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052602260045260246000fd5b610802806102076000396000f3fe608060405234801561001057600080fd5b50600436106100575760003560e01c806306fdde031461005c5780631249c58b1461007a57806390b98a111461008457806395d89b41146100b4578063f8b2cb4f146100d2575b600080fd5b610064610102565b6040516100719190610551565b60405180910390f35b610082610190565b005b61009e60048036038101906100999190610459565b6101e7565b6040516100ab9190610536565b60405180910390f35b6100bc61032b565b6040516100c99190610551565b60405180910390f35b6100ec60048036038101906100e7919061042c565b6103b9565b6040516100f99190610573565b60405180910390f35b6000805461010f906106af565b80601f016020809104026020016040519081016040528092919081815260200182805461013b906106af565b80156101885780601f1061015d57610100808354040283529160200191610188565b820191906000526020600020905b81548152906001019060200180831161016b57829003601f168201915b505050505081565b600260003273ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008154809291906101e0906106e1565b9190505550565b600081600260003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000205410156102395760009050610325565b81600260003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008282546102889190610600565b9250508190555081600260008573ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008282546102de91906105aa565b925050819055507fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef338484604051610318939291906104ff565b60405180910390a1600190505b92915050565b60018054610338906106af565b80601f0160208091040260200160405190810160405280929190818152602001828054610364906106af565b80156103b15780601f10610386576101008083540402835291602001916103b1565b820191906000526020600020905b81548152906001019060200180831161039457829003601f168201915b505050505081565b6000600260008373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020549050919050565b6000813590506104118161079e565b92915050565b600081359050610426816107b5565b92915050565b60006020828403121561044257610441610788565b5b600061045084828501610402565b91505092915050565b600080604083850312156104705761046f610788565b5b600061047e85828601610402565b925050602061048f85828601610417565b9150509250929050565b6104a281610634565b82525050565b6104b181610646565b82525050565b60006104c28261058e565b6104cc8185610599565b93506104dc81856020860161067c565b6104e58161078d565b840191505092915050565b6104f981610672565b82525050565b60006060820190506105146000830186610499565b6105216020830185610499565b61052e60408301846104f0565b949350505050565b600060208201905061054b60008301846104a8565b92915050565b6000602082019050818103600083015261056b81846104b7565b905092915050565b600060208201905061058860008301846104f0565b92915050565b600081519050919050565b600082825260208201905092915050565b60006105b582610672565b91506105c083610672565b9250827fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff038211156105f5576105f461072a565b5b828201905092915050565b600061060b82610672565b915061061683610672565b9250828210156106295761062861072a565b5b828203905092915050565b600061063f82610652565b9050919050565b60008115159050919050565b600073ffffffffffffffffffffffffffffffffffffffff82169050919050565b6000819050919050565b60005b8381101561069a57808201518184015260208101905061067f565b838111156106a9576000848401525b50505050565b600060028204905060018216806106c757607f821691505b602082108114156106db576106da610759565b5b50919050565b60006106ec82610672565b91507fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff82141561071f5761071e61072a565b5b600182019050919050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052601160045260246000fd5b7f4e487b7100000000000000000000000000000000000000000000000000000000600052602260045260246000fd5b600080fd5b6000601f19601f8301169050919050565b6107a781610634565b81146107b257600080fd5b50565b6107be81610672565b81146107c957600080fd5b5056fea26469706673582212207542c2f888f96a393f083a7e1836e8d9a2b4ba3f2b1e40e3a74634bf746dd6ff64736f6c63430008060033"

# # set pre-funded account as sender
web3.eth.defaultAccount = web3.eth.accounts[0]

# # Instantiate and deploy contract
MyContract = web3.eth.contract(abi=abi, bytecode=bytecode)

# # Submit the transaction that deploys the contract
tx_hash = MyContract.constructor().transact()

# # Wait for the transaction to be mined, and get the transaction receipt
tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)

# # Create the contract instance with the newly-deployed address
contract = web3.eth.contract(
    address=tx_receipt.contractAddress,
    abi=abi,
)

print(tx_receipt.contractAddress)

# # # # Display the default greeting from the contract
print('Default contract value: {}'.format(
    contract.functions.getBalance('0xCF716fAE671155d9663a8D2aC46BbBA4B537265d').call()
))

print(contract.functions.symbol().call())
print(contract.functions.name().call())

# # update the greeting
tx_hash = contract.functions.mint().transact()

# # Wait for transaction to be mined...
web3.eth.waitForTransactionReceipt(tx_hash)

# # Display the new greeting value
print('Updated contract value: {}'.format(
    contract.functions.getBalance('0xCF716fAE671155d9663a8D2aC46BbBA4B537265d').call()
))

# Truffle

## Hello Solidity script
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

## Migration script
const Hello= artifacts.require("hello");
module.exports = function (deployer) {
  deployer.deploy(Hello);
};

## Testing
Hello.deployed().then(function(instance) {return instance.store(255) });
Hello.deployed().then(function(instance) {return instance.retrieve() });

## Activity: 

## Adoption.sol
pragma solidity ^0.5.0;
contract Adoption {
    address[16] public adopters;
    // Adopting a pet
    function adopt(uint petId) public returns (uint) {
        require(petId >= 0 && petId <= 15);
        adopters[petId] = msg.sender;
        return petId;
        }
    // Retrieving the adopters
    function getAdopters() public view returns (address[16] memory) {
        return adopters;
        }
   }

### Migration

var Adoption = artifacts.require("Adoption");

module.exports = function(deployer) {
  deployer.deploy(Adoption);
};

### Remove the multi-line comment from within initWeb3 and replace it with the following:

// Modern dapp browsers...
if (window.ethereum) {
  App.web3Provider = window.ethereum;
  try {
    // Request account access
    await window.ethereum.enable();
  } catch (error) {
    // User denied account access...
    console.error("User denied account access")
  }
}
// Legacy dapp browsers...
else if (window.web3) {
  App.web3Provider = window.web3.currentProvider;
}
// If no injected web3 instance is detected, fall back to Ganache
else {
  App.web3Provider = new Web3.providers.HttpProvider('http://localhost:7545');
}
web3 = new Web3(App.web3Provider);

### Still in /src/js/app.js, remove the multi-line comment from within initContract and replace it with the following:
$.getJSON('Adoption.json', function(data) {
  // Get the necessary contract artifact file and instantiate it with @truffle/contract
  var AdoptionArtifact = data;
  App.contracts.Adoption = TruffleContract(AdoptionArtifact);

  // Set the provider for our contract
  App.contracts.Adoption.setProvider(App.web3Provider);

  // Use our contract to retrieve and mark the adopted pets
  return App.markAdopted();
});

### Still in /src/js/app.js, remove the multi-line comment from markAdopted and replace it with the following:

var adoptionInstance;

App.contracts.Adoption.deployed().then(function(instance) {
  adoptionInstance = instance;

  return adoptionInstance.getAdopters.call();
}).then(function(adopters) {
  for (i = 0; i < adopters.length; i++) {
    if (adopters[i] !== '0x0000000000000000000000000000000000000000') {
      $('.panel-pet').eq(i).find('button').text('Success').attr('disabled', true);
    }
  }
}).catch(function(err) {
  console.log(err.message);
});

### Still in /src/js/app.js, remove the multi-line comment from handleAdopt and replace it with the following:

var adoptionInstance;

web3.eth.getAccounts(function(error, accounts) {
  if (error) {
    console.log(error);
  }

  var account = accounts[0];

  App.contracts.Adoption.deployed().then(function(instance) {
    adoptionInstance = instance;

    // Execute adopt as a transaction by sending account
    return adoptionInstance.adopt(petId, {from: account});
  }).then(function(result) {
    return App.markAdopted();
  }).catch(function(err) {
    console.log(err.message);
  });
});