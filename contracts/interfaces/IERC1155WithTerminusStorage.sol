// SPDX-License-Identifier: Apache-2.0

pragma solidity ^0.8.0;

import "./IERC1155MetadataURI.sol";

interface IERC1155WithTerminusStorage is IERC1155, IERC1155MetadataURI {
    function isApprovedForPool(uint256 poolID, address operator)
        external
        view
        returns (bool);
}
