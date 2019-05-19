pragma solidity >=0.4.16 <0.6.0;

contract ApprovalContract {

  address public sender;
  address public receiver;
  address constant public approver = 0x2DDeB9FCA46B4c143ec91c21b7c71084FE90D48c;

  function deposit(address _receiver) external payable {
    require(msg.value > 0);
    sender = msg.sender;
    receiver = _receiver;
  }

  function viewApprover() external pure returns(address payable[] memory) {
    return(approver);
  }

  function approve() external {
    require(msg.sender == approver);
    receiver.transfer(address(this).balance);
  }

}
