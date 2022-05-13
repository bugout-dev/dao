// SPDX-License-Identifier: Apache-2.0

/**
 * Authors: Moonstream Engineering (engineering@moonstream.to)
 * GitHub: https://github.com/bugout-dev/dao
 *
 * Initializer for Moonstream DAO platform token. Used when mounting a new ERC20Facet onto its
 * diamond proxy.
 */

pragma solidity ^0.8.0;

import "@openzeppelin-contracts/contracts/token/ERC20/IERC20.sol";
import "../diamond/libraries/LibDiamond.sol";
import "./LibERC20.sol";

contract ERC20Initializer {
    function init(string memory name, string memory symbol) external {
        LibDiamond.DiamondStorage storage ds = LibDiamond.diamondStorage();
        ds.supportedInterfaces[type(IERC20).interfaceId] = true;

        LibERC20.ERC20Storage storage es = LibERC20.erc20Storage();
        es.controller = msg.sender;
        es.name = name;
        es.symbol = symbol;
    }
}
