// SPDX-License-Identifier: Apache-2.0

/**
 * Authors: Moonstream Engineering (engineering@moonstream.to)
 * GitHub: https://github.com/bugout-dev/dao
 *
 */

import "@openzeppelin-contracts/contracts/access/Ownable.sol";
import "../interfaces/ITerminus.sol";

pragma solidity ^0.8.9;

abstract contract TerminusPermissions {
    function _holdsPoolToken(
        address terminusAddress,
        uint256 poolId,
        uint256 _amount
    ) internal view returns (bool) {
        ITerminus terminus = ITerminus(terminusAddress);
        return terminus.balanceOf(msg.sender, poolId) >= _amount;
    }

    modifier holdsPoolToken(address terminusAddress, uint256 poolId) {
        require(
            _holdsPoolToken(terminusAddress, poolId, 1),
            "TerminusPermissions.holdsPoolToken: Sender doens't hold  pool tokens"
        );
        _;
    }

    modifier spendsPoolToken(address terminusAddress, uint256 poolId) {
        require(
            _holdsPoolToken(terminusAddress, poolId, 1),
            "TerminusPermissions.spendsPoolToken: Sender doens't hold  pool tokens"
        );
        ITerminus terminusContract = ITerminus(terminusAddress);
        terminusContract.burn(msg.sender, poolId, 1);
        _;
    }
}
