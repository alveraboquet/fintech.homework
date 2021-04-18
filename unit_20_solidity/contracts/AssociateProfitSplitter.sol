pragma solidity ^0.5.0;

import "github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/math/SafeMath.sol";

// lvl 1: equal split
contract AssociateProfitSplitter {
    
    using SafeMath for uint;

    address payable employee_one;
    address payable employee_two;
    address payable employee_three;
    
    address payable owner;
    
    modifier onlyOwner {
        require(msg.sender == owner, "You do not have permission to mint these tokens!");
        _;
    }
    
    constructor(address payable _one, address payable _two, address payable _three) public {
        employee_one = _one;
        employee_two = _two;
        employee_three = _three;
        owner = msg.sender;
    }

    function balance() public view returns(uint) {
        return address(this).balance;
    }

    function deposit() public payable onlyOwner {
        
        // Calculate the split value of the Ether for each employee
        uint amount = msg.value.div(3); 
        
        // Transfer the amount to each employee
        employee_one.transfer(amount);
        employee_two.transfer(amount);
        employee_three.transfer(amount);
        
        // Take care of a potential remainder by sending back to HR (`msg.sender`)
        // Note: Since uint only contains positive whole numbers, and Solidity does not fully support float/decimals, 
        // we must deal with a potential remainder at the end of this function since amount will discard the remainder during division.
        msg.sender.transfer(msg.value.sub(amount.mul(3)));
    }
    
    function() external payable {
    
        // Enforce that the `deposit` function is called in the fallback function!
        deposit();
    }
}
