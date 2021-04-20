pragma solidity ^0.5.0;

import "github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/math/SafeMath.sol";

// lvl 3: equity plan
contract DeferredEquityPlan {
    
    // Local testing, remove in PROD
    uint public fakenow = now;
    
    using SafeMath for uint;
    
    address human_resources;
    
    // Bob
    address payable employee; 
    
    // This employee is active at the start of the contract
    bool active = true; 
    
    // Total shares
    uint total_shares = 1000;
    
    // Annual distribution
    uint annual_distribution = 250;
    
    // Permanently store the time this contract was initialized
    //uint start_time = now; 
    uint start_time = fakenow; 
    
    // `unlock_time` is 365 days from now
    //uint unlock_time = now.add(365);
    uint unlock_time = fakenow.add(365);
    
    // Starts at 0
    uint public distributed_shares = 0; 

    constructor(address payable _employee) public {
        human_resources = msg.sender;
        employee = _employee;
    }

    function distribute() public {
        require(msg.sender == human_resources || msg.sender == employee, "You are not authorized to execute this contract.");
        require(active == true, "Contract not active.");
        
        // 1: `unlock_time` is less than or equal to `now`
        //require(unlock_time <= now, "Account currently locked.");
        require(unlock_time <= fakenow, "Account currently locked.");
        
        // 2: `distributed_shares` is less than the `total_shares`
        require(distributed_shares < total_shares, "You are fully vested.");
        
        // Add 365 days to the `unlock_time`
        unlock_time += 365;
        
        // Calculate the shares distributed by using the function (now - start_time) / 365 days * the annual distribution
        // Make sure to include the parenthesis around (now - start_time) to get accurate results!
        //distributed_shares = (now.sub(start_time)).div(365).mul(annual_distribution);
        distributed_shares = (fakenow.sub(start_time)).div(365).mul(annual_distribution);
        
        // double check in case the employee does not cash out until after 5+ years
        if (distributed_shares > 1000) {
            distributed_shares = 1000;
        }
    }
    
    function fastforward() public {
        fakenow += 100 days;
    }


    // human_resources and the employee can deactivate this contract at-will
    function deactivate() public {
        require(msg.sender == human_resources || msg.sender == employee, "You are not authorized to deactivate this contract.");
        active = false;
    }

    // Since we do not need to handle Ether in this contract, revert any Ether sent to the contract directly
    function() external payable {
        revert("Do not send Ether to this contract!");
    }
}
