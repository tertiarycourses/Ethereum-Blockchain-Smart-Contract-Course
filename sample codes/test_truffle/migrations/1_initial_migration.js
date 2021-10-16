const Hello= artifacts.require("hello");

module.exports = function (deployer) {
  deployer.deploy(Hello);
};

