const HDWalletProvider = require("@truffle/hdwallet-provider");
var mnemonic = "ugly goat resemble trophy receive series tired churn annual increase kingdom minimum";

module.exports = {
  networks: {
   development: {
    host: "127.0.0.1",
    port: 7545,
    network_id: "*"
   },
   ropsten: {
       provider: function() { 
        return new HDWalletProvider(mnemonic, "https://rinkeby.infura.io/v3/95408920a948489c99c5bcb436235bd2");
       },
       network_id: 4,
       gas: 4500000,
       gasPrice: 10000000000,
   },
//    live: {
//     provider: function() { 
//      return new HDWalletProvider(mnemonic, "https://mainnet.infura.io/v3/db7278945d1741a4963fdcaa6a0c47e6");
//     },
//     network_id: 1,
//     gas: 7500000,
//     gasPrice: 10000000000,
// }
  }
 };
