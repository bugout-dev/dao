// SPDX-License-Identifier: Apache-2.0

/**
 * Authors: Moonstream Engineering (engineering@moonstream.to)
 * GitHub: https://github.com/bugout-dev/dao
 *
 * This is an implementation of the ERC20 platform token for the Moonstream DAO.
 */

pragma solidity ^0.8.0;

import "./ERC20WithCommonStorage.sol";
import "./LibERC20.sol";
import "../diamond/libraries/LibDiamond.sol";

contract ERC20Facet is ERC20WithCommonStorage {
    constructor() {}

    function moonstreamController() external view returns (address) {
        return LibERC20.erc20Storage().controller;
    }

    function mint(address account, uint256 amount) external {
        LibERC20.enforceIsController();
        _mint(account, amount);
    }

    function batchMint(address[] calldata accounts, uint256 amount) external {
        LibERC20.enforceIsController();
        _batchMint(accounts, amount);
    }
}
