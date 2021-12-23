// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

import {IERC20} from "@openzeppelin-contracts/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin-contracts/contracts/access/Ownable.sol";

contract MoonstreamTokenFaucet is Ownable {
    address MOONSTREAM_TOKEN_ADDRESS;
    uint256 FAUCET_AMOUNT;
    uint256 FAUCET_BLOCK_INTERVAL;
    mapping(address => uint256) lastClaimedBlock;

    constructor(
        address _MOONSTREAM_TOKEN_ADDRESS,
        address owner,
        uint256 _FAUCET_AMOUNT,
        uint256 _FAUCET_BLOCK_INTERVAL
    ) {
        MOONSTREAM_TOKEN_ADDRESS = _MOONSTREAM_TOKEN_ADDRESS;
        FAUCET_AMOUNT = _FAUCET_AMOUNT;
        FAUCET_BLOCK_INTERVAL = _FAUCET_BLOCK_INTERVAL;
        transferOwnership(owner);
    }

    function getMoonstreamTokenAddress() public view returns (address) {
        return MOONSTREAM_TOKEN_ADDRESS;
    }

    function getMoonstreamToken() internal view returns (IERC20) {
        return IERC20(MOONSTREAM_TOKEN_ADDRESS);
    }

    function getMoonstreamTokenBalance(address _address)
        public
        view
        returns (uint256)
    {
        return getMoonstreamToken().balanceOf(_address);
    }

    function getLastClaimedBlock(address _address)
        public
        view
        returns (uint256)
    {
        return lastClaimedBlock[_address];
    }

    function claim() public {
        uint256 current_block = block.number;
        require(
            current_block > lastClaimedBlock[msg.sender] + FAUCET_BLOCK_INTERVAL
        );
        getMoonstreamToken().transfer(msg.sender, FAUCET_AMOUNT);
        lastClaimedBlock[msg.sender] = current_block;
    }

    function getFaucetAmount() public view returns (uint256) {
        return FAUCET_AMOUNT;
    }

    function getFaucetBlockInterval() public view returns (uint256) {
        return FAUCET_BLOCK_INTERVAL;
    }

    function setFaucetBlockInterval(uint256 _FAUCET_BLOCK_INTERVAL)
        public
        onlyOwner
    {
        FAUCET_BLOCK_INTERVAL = _FAUCET_BLOCK_INTERVAL;
    }

    function setFaucetAmount(uint256 _FAUCET_AMOUNT) public onlyOwner {
        FAUCET_AMOUNT = _FAUCET_AMOUNT;
    }

    function setMoonstreamTokenAddress(address _MOONSTREAM_TOKEN_ADDRESS)
        public
        onlyOwner
    {
        MOONSTREAM_TOKEN_ADDRESS = _MOONSTREAM_TOKEN_ADDRESS;
    }
}
