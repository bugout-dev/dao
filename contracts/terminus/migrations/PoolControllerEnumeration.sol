// SPDX-License-Identifier: Apache-2.0

/**
 * Authors: Moonstream Engineering (engineering@moonstream.to)
 * GitHub: https://github.com/bugout-dev/dao
 *
 * Migration file to migrate upgrade where we add terminus pool controller enumeration functionality
 */

pragma solidity ^0.8.9;

import "../LibTerminus.sol";
import "../../diamond/libraries/LibDiamond.sol";
import "../IERC1155Enumerable.sol";

contract PoolControllerEnumeration {
    function init() external {
        LibDiamond.DiamondStorage storage ds = LibDiamond.diamondStorage();
        ds.supportedInterfaces[type(IERC1155Enumerable).interfaceId] = true;

        LibTerminus.TerminusStorage storage ts = LibTerminus.terminusStorage();

        for (uint256 i = 0; i < (ts.currentPoolID+1); i++) {
            address poolController = ts.poolController[i];
            ts.controllerPoolsNumber[poolController]++;
            ts.controlledPools[poolController][
                ts.controllerPoolsNumber[poolController]
            ] = i;
            ts.fromPoolIdToControllersPoolId[i] = ts.controllerPoolsNumber[poolController];
        }
    }
}
