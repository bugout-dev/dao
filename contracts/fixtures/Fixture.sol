// SPDX-License-Identifier: Apache-2.0

/**
 * Authors: Moonstream Engineering (engineering@moonstream.to)
 * GitHub: https://github.com/bugout-dev/dao
 *
 * Fixture contract to check in test enviroment that connected contract is indeed test fixture
 */

pragma solidity ^0.8.9;

contract TestFixture {
    function isFixture () public pure returns (bool)
    {
        return true;
    }
}
