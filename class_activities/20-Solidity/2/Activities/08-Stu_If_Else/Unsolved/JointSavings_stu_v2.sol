pragma solidity ^0.5.0;

contract JointSavings {
  address payable account_one = 0xc3879B456DAA348a16B6524CBC558d2CC984722c;
  address payable account_two = 0xA29f7E79ECEA4cE30DD78cfeb9605D9aFf5143a5;

  uint public balanceContract;
  
  function withdraw(uint amount, address payable recipient) public {
    recipient.transfer(amount);
    balanceContract = address(this).balance;
  }

  function deposit() public payable {
    balanceContract = address(this).balance;
  }

  function() external payable {}

}