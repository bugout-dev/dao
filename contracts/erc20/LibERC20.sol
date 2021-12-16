// SPDX-License-Identifier: Apache-2.0
pragma solidity ^0.8.9;

library LibDiamond {
    bytes32 constant ERC20_STORAGE_POSITION =
        keccak256("moonstreamdao.eth.storage.erc20");

    struct ERC20Storage {
        address controller;
        uint256 totalSupply;
        string name;
        string symbol;
        mapping(address => uint256) balances;
        mapping(address => mapping(address => uint256)) allowances;
    }

    function erc20Storage() internal pure returns (ERC20Storage storage es) {
        bytes32 position = ERC20_STORAGE_POSITION;
        assembly {
            es.slot := position
        }
    }

    event ControlTransferred(
        address indexed previousController,
        address indexed newController
    );

    function setController(address _newController) internal {
        ERC20Storage storage es = erc20Storage();
        address previousController = es.controller;
        es.controller = _newController;
        emit ControlTransferred(previousController, _newController);
    }

    function getController()
        internal
        view
        returns (address contractController_)
    {
        contractController_ = erc20Storage().controller;
    }

    function enforceIsController() internal view {
        ERC20Storage storage es = erc20Storage();
        require(msg.sender == es.controller, "LibERC20: Must be controller");
    }
}
