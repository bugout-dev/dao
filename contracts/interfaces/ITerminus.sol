// SPDX-License-Identifier: Apache-2.0

pragma solidity ^0.8.0;
import "./IERC1155WithTerminusStorage.sol";

interface ITerminus is IERC1155WithTerminusStorage {
    event PoolMintBatch(
        uint256 indexed id,
        address indexed operator,
        address from,
        address[] toAddresses,
        uint256[] amounts
    );

    function setController(address newController) external;

    function poolMintBatch(
        uint256 id,
        address[] memory toAddresses,
        uint256[] memory amounts
    ) external;

    function terminusController() external view returns (address);

    function paymentToken() external view returns (address);

    function setPaymentToken(address newPaymentToken) external;

    function poolBasePrice() external view returns (uint256);

    function setPoolBasePrice(uint256 newBasePrice) external;

    function withdrawPayments(address toAddress, uint256 amount) external;

    function contractURI() external view returns (string memory);

    function setContractURI(string memory _contractURI) external;

    function setURI(uint256 poolID, string memory poolURI) external;

    function totalPools() external view returns (uint256);

    function setPoolController(uint256 poolID, address newController) external;

    function terminusPoolController(uint256 poolID)
        external
        view
        returns (address);

    function terminusPoolCapacity(uint256 poolID)
        external
        view
        returns (uint256);

    function terminusPoolSupply(uint256 poolID) external view returns (uint256);

    function createSimplePool(uint256 _capacity) external returns (uint256);

    function createPoolV1(
        uint256 _capacity,
        bool _transferable,
        bool _burnable
    ) external returns (uint256);

    function mint(
        address to,
        uint256 poolID,
        uint256 amount,
        bytes memory data
    ) external;

    function mintBatch(
        address to,
        uint256[] memory poolIDs,
        uint256[] memory amounts,
        bytes memory data
    ) external;

    function burn(
        address from,
        uint256 poolID,
        uint256 amount
    ) external;
}
