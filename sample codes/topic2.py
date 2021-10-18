# Topic 2 : Web3.py

from web3 import Web3

## Fill in your infura API key here
infura_url = "https://mainnet.infura.io/v3/XXXXXXX"
web3 = Web3(Web3.HTTPProvider(infura_url))

print(f'Connnected to Web3: {web3.isConnected()}')
print(f'Latest block numebr: {web3.eth.blockNumber}')
print(f'Latest gas price: {web3.eth.gasPrice}')

# Activity: Web3.py ** 

from web3 import Web3

infura_url = "https://mainnet.infura.io/v3/XXXXXXX"
web3 = Web3(Web3.HTTPProvider(infura_url))

print(web3.eth.getBlock(13439096))

## Demo: Check Wallet balnace ##

from web3 import Web3

## Fill in your infura API key here
# infura_url = "https://mainnet.infura.io/v3/XXXXXXX"
infuria_url= "https://rinkeby.infura.io/v3/XXXX"
web3 = Web3(Web3.HTTPProvider(infura_url))

# # Fill in your account here
balance = web3.eth.getBalance("0xec914D5a21EeC7692a985E80207Df05CdD1E2CE5")
print(web3.fromWei(balance, "ether"))


## Demo: Get info from OMG Token ##
import json
from web3 import Web3

## Fill in your infura API key here
infura_url = "https://mainnet.infura.io/v3/XXXXXXX"
web3 = Web3(Web3.HTTPProvider(infura_url))

# OMG ABI
abi = json.loads('[{"constant":true,"inputs":[],"name":"mintingFinished","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint256"}],"payable":false,"type":"function"},{"constant":false,"inputs":[],"name":"unpause","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_amount","type":"uint256"}],"name":"mint","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"paused","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"payable":false,"type":"function"},{"constant":false,"inputs":[],"name":"finishMinting","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":false,"inputs":[],"name":"pause","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_amount","type":"uint256"},{"name":"_releaseTime","type":"uint256"}],"name":"mintTimelocked","outputs":[{"name":"","type":"address"}],"payable":false,"type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"remaining","type":"uint256"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"payable":false,"type":"function"},{"anonymous":false,"inputs":[{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Mint","type":"event"},{"anonymous":false,"inputs":[],"name":"MintFinished","type":"event"},{"anonymous":false,"inputs":[],"name":"Pause","type":"event"},{"anonymous":false,"inputs":[],"name":"Unpause","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"owner","type":"address"},{"indexed":true,"name":"spender","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Transfer","type":"event"}]')

# OMG Contract address
address = '0xd26114cd6EE289AccF82350c8d8487fedB8A0C07'

contract = web3.eth.contract(address=address, abi=abi)
totalSupply = contract.functions.totalSupply().call()
balance = contract.functions.balanceOf(address).call()

print(f'Token Name: {contract.functions.name().call()}')
print(f'Token Symbol: {contract.functions.symbol().call()}')
print(f'Token Supply: {web3.fromWei(totalSupply, "ether")} ether')
print(f'Token Balance: {web3.fromWei(balance, "ether")} ether')

## Activity: Bancor Token ##
import json
from web3 import Web3

## Fill in your infura API key here
infura_url = "https://mainnet.infura.io/v3/XXXXXXX"
web3 = Web3(Web3.HTTPProvider(infura_url))

abi = json.loads('[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[{"name":"success","type":"bool"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_disable","type":"bool"}],"name":"disableTransfers","outputs":[],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"success","type":"bool"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"version","outputs":[{"name":"","type":"string"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"standard","outputs":[{"name":"","type":"string"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_token","type":"address"},{"name":"_to","type":"address"},{"name":"_amount","type":"uint256"}],"name":"withdrawTokens","outputs":[],"payable":false,"type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"type":"function"},{"constant":false,"inputs":[],"name":"acceptOwnership","outputs":[],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_amount","type":"uint256"}],"name":"issue","outputs":[],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_amount","type":"uint256"}],"name":"destroy","outputs":[],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[{"name":"success","type":"bool"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"transfersEnabled","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"newOwner","outputs":[{"name":"","type":"address"}],"payable":false,"type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"},{"name":"","type":"address"}],"name":"allowance","outputs":[{"name":"","type":"uint256"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"payable":false,"type":"function"},{"inputs":[{"name":"_name","type":"string"},{"name":"_symbol","type":"string"},{"name":"_decimals","type":"uint8"}],"payable":false,"type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"name":"_token","type":"address"}],"name":"NewSmartToken","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"_amount","type":"uint256"}],"name":"Issuance","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"_amount","type":"uint256"}],"name":"Destruction","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"_prevOwner","type":"address"},{"indexed":false,"name":"_newOwner","type":"address"}],"name":"OwnerUpdate","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"_from","type":"address"},{"indexed":true,"name":"_to","type":"address"},{"indexed":false,"name":"_value","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"_owner","type":"address"},{"indexed":true,"name":"_spender","type":"address"},{"indexed":false,"name":"_value","type":"uint256"}],"name":"Approval","type":"event"}]')
address = '0x1F573D6Fb3F13d689FF844B4cE37794d79a7FF1C'

contract = web3.eth.contract(address=address, abi=abi)
totalSupply = contract.functions.totalSupply().call()
balance = contract.functions.balanceOf(address).call()

print(f'Token Name: {contract.functions.name().call()}')
print(f'Token Symbol: {contract.functions.symbol().call()}')
print(f'Token Supply: {web3.fromWei(totalSupply, "ether")} ether')
print(f'Token Balance: {web3.fromWei(balance, "ether")} ether')

## Demo: Compile Hello World Smart Contract on Ganache blockchain ##
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

## Demo: Compile Hello World Smart Contract on Ganache blockchain ##
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

# Activity: Transact Contract on Smart Contract
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

## Demo: Transfer Etehr between 2 accounts on Ganache ##

from web3 import Web3

ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

account_1 = 'XXXX' # Fill me in
account_2 = 'XXXX' # Fill me in
private_key = 'XXXX' # Fill me in

nonce = web3.eth.getTransactionCount(account_1)

# Step1: Create the transaction
tx = {
    'nonce': nonce,
    'to': account_2,
    'value': web3.toWei(5, 'ether'),
    'gas': 2000000,
    'gasPrice': web3.toWei('50', 'gwei'),
}

# Step2: Sign the transaction
signed_tx = web3.eth.account.signTransaction(tx, private_key)

# Step 3: Send the transaction
tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)

print(web3.toHex(tx_hash))

# Activity: Transfer Etehr between 2 accounts on Ganache ## 

from web3 import Web3

ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

account_1 = 'XXXX' # Fill me in
account_2 = 'XXXX' # Fill me in
private_key = 'XXX # Fill me in

nonce = web3.eth.getTransactionCount(account_1)

# Sign the transaction
tx = {
    'nonce': nonce,
    'to': account_2,
    'value': web3.toWei(5, 'ether'),
    'gas': 2000000,
    'gasPrice': web3.toWei('50', 'gwei'),
}

# Sign the transaction
signed_tx = web3.eth.account.signTransaction(tx, private_key)

# Send the transaction
tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)

print(web3.toHex(tx_hash))

# Test Transaction with Web3
### Deploy the smart contract on Remix to Ganache
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

### Get the contract address and abi from Remix, test transaction with web3 
import json
from web3 import Web3

## Connect to Ganahe
ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

# Set a default account to sign transaction
web3.eth.defaultAccount = web3.eth.accounts[0]

# Contract ABI
abi = json.loads('[{"inputs":[],"name":"myString","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"retrieve","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"_myString","type":"string"}],"name":"store","outputs":[],"stateMutability":"nonpayable","type":"function"}]')

# Contract address
address = web3.toChecksumAddress('0xf3d789a8B6435D2Efa878eb139ceFe4b3a277494') # FILL ME IN

# Initialize contract
contract = web3.eth.contract(address=address, abi=abi)

# Store value 
tx_hash = contract.functions.store('Good Day').transact()

# Wait for transaction to be mined
web3.eth.waitForTransactionReceipt(tx_hash)

# Retrieve value
print(f'Retrive the value: {contract.functions.retrieve().call()}')


# Acitivty: Test Transaction with Web3

### Deploy the smart contract on Remix to Ganache
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

### Get the contract address and abi from Remix, test transaction with web3
import json
from web3 import Web3

# Set up web3 connection with Ganache
import json
from web3 import Web3

# Set up web3 connection with Ganache
ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

# Set a default account to sign transaction
web3.eth.defaultAccount = web3.eth.accounts[0]

# Contract ABI
abi = json.loads('[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"retrieve","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"num","type":"uint256"}],"name":"store","outputs":[],"stateMutability":"nonpayable","type":"function"}]')

# Contract address
address = web3.toChecksumAddress('0x89F770e449653f1A9977B0DE1132d245c8AD0Feb')

# Initialize contract
contract = web3.eth.contract(address=address, abi=abi)

# Store value 
tx_hash = contract.functions.store(255).transact()

# Wait for transaction to be mined
web3.eth.waitForTransactionReceipt(tx_hash)

# Retrieve value
print(f'Retrive the value: {contract.functions.retrieve().call()}')






