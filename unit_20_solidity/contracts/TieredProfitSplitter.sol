pragma solidity ^0.5.0;

import "github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/math/SafeMath.sol";

// lvl 2: tiered split
contract TieredProfitSplitter {
    
    using SafeMath for uint;
    
    // Contract owner (HR)
    address payable owner;
    
    // CEO
    address payable employee_one; 
    
    // CTO
    address payable employee_two; 
    
    // Bob
    address payable employee_three; 


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

    // Should always return 0! Use this to test your `deposit` function's logic
    function balance() public view returns(uint) {
        return address(this).balance;
    }

    function deposit() public payable onlyOwner {
        
        // Calculates rudimentary percentage by dividing msg.value into 100 units
        uint points = msg.value.div(100);
        uint total = 0;
        uint amount = 0;

        // Empoyee 1 (CEO)
        amount = points.mul(60);
        total += amount;
        employee_one.transfer(amount);
        
        // Empoyee 2 (CTO)
        amount = points.mul(25);
        total += amount;
        employee_two.transfer(amount);
        
        // Empoyee 3 (Bob)
        amount = points.mul(15);
        total += amount;
        employee_three.transfer(amount);

        // Return remainder wei to CEO
        employee_one.transfer(msg.value - total);
    }

    function() external payable {
        deposit();
    }
}
