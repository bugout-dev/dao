# Code generated by moonworm : https://github.com/bugout-dev/moonworm
# Moonworm version : 0.6.2

import argparse
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from brownie import Contract, network, project
from brownie.network.contract import ContractContainer
from eth_typing.evm import ChecksumAddress


PROJECT_DIRECTORY = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BUILD_DIRECTORY = os.path.join(PROJECT_DIRECTORY, "build", "contracts")


def boolean_argument_type(raw_value: str) -> bool:
    TRUE_VALUES = ["1", "t", "y", "true", "yes"]
    FALSE_VALUES = ["0", "f", "n", "false", "no"]

    if raw_value.lower() in TRUE_VALUES:
        return True
    elif raw_value.lower() in FALSE_VALUES:
        return False

    raise ValueError(
        f"Invalid boolean argument: {raw_value}. Value must be one of: {','.join(TRUE_VALUES + FALSE_VALUES)}"
    )


def bytes_argument_type(raw_value: str) -> str:
    return raw_value


def get_abi_json(abi_name: str) -> List[Dict[str, Any]]:
    abi_full_path = os.path.join(BUILD_DIRECTORY, f"{abi_name}.json")
    if not os.path.isfile(abi_full_path):
        raise IOError(
            f"File does not exist: {abi_full_path}. Maybe you have to compile the smart contracts?"
        )

    with open(abi_full_path, "r") as ifp:
        build = json.load(ifp)

    abi_json = build.get("abi")
    if abi_json is None:
        raise ValueError(f"Could not find ABI definition in: {abi_full_path}")

    return abi_json


def contract_from_build(abi_name: str) -> ContractContainer:
    # This is workaround because brownie currently doesn't support loading the same project multiple
    # times. This causes problems when using multiple contracts from the same project in the same
    # python project.
    PROJECT = project.main.Project("moonworm", Path(PROJECT_DIRECTORY))

    abi_full_path = os.path.join(BUILD_DIRECTORY, f"{abi_name}.json")
    if not os.path.isfile(abi_full_path):
        raise IOError(
            f"File does not exist: {abi_full_path}. Maybe you have to compile the smart contracts?"
        )

    with open(abi_full_path, "r") as ifp:
        build = json.load(ifp)

    return ContractContainer(PROJECT, build)


class TerminusControllerFacet:
    def __init__(self, contract_address: Optional[ChecksumAddress]):
        self.contract_name = "TerminusControllerFacet"
        self.address = contract_address
        self.contract = None
        self.abi = get_abi_json("TerminusControllerFacet")
        if self.address is not None:
            self.contract: Optional[Contract] = Contract.from_abi(
                self.contract_name, self.address, self.abi
            )

    def deploy(self, transaction_config):
        contract_class = contract_from_build(self.contract_name)
        deployed_contract = contract_class.deploy(transaction_config)
        self.address = deployed_contract.address
        self.contract = deployed_contract
        return deployed_contract.tx

    def assert_contract_is_instantiated(self) -> None:
        if self.contract is None:
            raise Exception("contract has not been instantiated")

    def verify_contract(self):
        self.assert_contract_is_instantiated()
        contract_class = contract_from_build(self.contract_name)
        contract_class.publish_source(self.contract)

    def approve_for_pool(
        self, pool_id: int, operator: ChecksumAddress, transaction_config
    ) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.approveForPool(pool_id, operator, transaction_config)

    def balance_of(
        self,
        account: ChecksumAddress,
        id: int,
        block_number: Optional[Union[str, int]] = "latest",
    ) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.balanceOf.call(account, id, block_identifier=block_number)

    def burn(
        self, from_: ChecksumAddress, pool_id: int, amount: int, transaction_config
    ) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.burn(from_, pool_id, amount, transaction_config)

    def contract_uri(self, block_number: Optional[Union[str, int]] = "latest") -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.contractURI.call(block_identifier=block_number)

    def create_pool_v1(
        self, _capacity: int, _transferable: bool, _burnable: bool, transaction_config
    ) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.createPoolV1(
            _capacity, _transferable, _burnable, transaction_config
        )

    def create_simple_pool(self, _capacity: int, transaction_config) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.createSimplePool(_capacity, transaction_config)

    def drain_erc1155(
        self,
        token_address: ChecksumAddress,
        token_id: int,
        receiver_address: ChecksumAddress,
        transaction_config,
    ) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.drainERC1155(
            token_address, token_id, receiver_address, transaction_config
        )

    def drain_erc20(
        self,
        token_address: ChecksumAddress,
        receiver_address: ChecksumAddress,
        transaction_config,
    ) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.drainERC20(
            token_address, receiver_address, transaction_config
        )

    def get_terminus_address(
        self, block_number: Optional[Union[str, int]] = "latest"
    ) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.getTerminusAddress.call(block_identifier=block_number)

    def get_terminus_main_admin_pool_id(
        self, block_number: Optional[Union[str, int]] = "latest"
    ) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.getTerminusMainAdminPoolId.call(
            block_identifier=block_number
        )

    def get_terminus_pool_controller_pool(
        self, pool_id: int, block_number: Optional[Union[str, int]] = "latest"
    ) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.getTerminusPoolControllerPool.call(
            pool_id, block_identifier=block_number
        )

    def init_terminus_controller(
        self,
        terminus_address: ChecksumAddress,
        _terminus_main_admin_pool_terminus_address: ChecksumAddress,
        _terminus_main_admin_pool_id: int,
        transaction_config,
    ) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.initTerminusController(
            terminus_address,
            _terminus_main_admin_pool_terminus_address,
            _terminus_main_admin_pool_id,
            transaction_config,
        )

    def is_approved_for_pool(
        self,
        pool_id: int,
        operator: ChecksumAddress,
        block_number: Optional[Union[str, int]] = "latest",
    ) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.isApprovedForPool.call(
            pool_id, operator, block_identifier=block_number
        )

    def mint(
        self,
        to: ChecksumAddress,
        pool_id: int,
        amount: int,
        data: bytes,
        transaction_config,
    ) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.mint(to, pool_id, amount, data, transaction_config)

    def mint_batch(
        self,
        to: ChecksumAddress,
        pool_i_ds: List,
        amounts: List,
        data: bytes,
        transaction_config,
    ) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.mintBatch(to, pool_i_ds, amounts, data, transaction_config)

    def pool_mint_batch(
        self, id: int, to_addresses: List, amounts: List, transaction_config
    ) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.poolMintBatch(
            id, to_addresses, amounts, transaction_config
        )

    def set_contract_uri(self, _contract_uri: str, transaction_config) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.setContractURI(_contract_uri, transaction_config)

    def set_controller(
        self, new_controller: ChecksumAddress, transaction_config
    ) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.setController(new_controller, transaction_config)

    def set_pool_control_permissions(
        self,
        pool_id: int,
        terminus_address: ChecksumAddress,
        pool_controller_pool_id: int,
        transaction_config,
    ) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.setPoolControlPermissions(
            pool_id, terminus_address, pool_controller_pool_id, transaction_config
        )

    def set_pool_controller(
        self, pool_id: int, new_controller: ChecksumAddress, transaction_config
    ) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.setPoolController(
            pool_id, new_controller, transaction_config
        )

    def set_uri(self, pool_id: int, pool_uri: str, transaction_config) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.setURI(pool_id, pool_uri, transaction_config)

    def terminus_controller(
        self, block_number: Optional[Union[str, int]] = "latest"
    ) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.terminusController.call(block_identifier=block_number)

    def terminus_pool_capacity(
        self, pool_id: int, block_number: Optional[Union[str, int]] = "latest"
    ) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.terminusPoolCapacity.call(
            pool_id, block_identifier=block_number
        )

    def terminus_pool_controller(
        self, pool_id: int, block_number: Optional[Union[str, int]] = "latest"
    ) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.terminusPoolController.call(
            pool_id, block_identifier=block_number
        )

    def terminus_pool_supply(
        self, pool_id: int, block_number: Optional[Union[str, int]] = "latest"
    ) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.terminusPoolSupply.call(
            pool_id, block_identifier=block_number
        )

    def total_pools(self, block_number: Optional[Union[str, int]] = "latest") -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.totalPools.call(block_identifier=block_number)

    def unapprove_for_pool(
        self, pool_id: int, operator: ChecksumAddress, transaction_config
    ) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.unapproveForPool(pool_id, operator, transaction_config)

    def withdraw_erc1155(
        self,
        token_address: ChecksumAddress,
        token_id: int,
        amount: int,
        receiver_address: ChecksumAddress,
        transaction_config,
    ) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.withdrawERC1155(
            token_address, token_id, amount, receiver_address, transaction_config
        )

    def withdraw_erc20(
        self,
        token_address: ChecksumAddress,
        amount: int,
        receiver_address: ChecksumAddress,
        transaction_config,
    ) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.withdrawERC20(
            token_address, amount, receiver_address, transaction_config
        )


def get_transaction_config(args: argparse.Namespace) -> Dict[str, Any]:
    signer = network.accounts.load(args.sender, args.password)
    transaction_config: Dict[str, Any] = {"from": signer}
    if args.gas_price is not None:
        transaction_config["gas_price"] = args.gas_price
    if args.max_fee_per_gas is not None:
        transaction_config["max_fee"] = args.max_fee_per_gas
    if args.max_priority_fee_per_gas is not None:
        transaction_config["priority_fee"] = args.max_priority_fee_per_gas
    if args.confirmations is not None:
        transaction_config["required_confs"] = args.confirmations
    if args.nonce is not None:
        transaction_config["nonce"] = args.nonce
    return transaction_config


def add_default_arguments(parser: argparse.ArgumentParser, transact: bool) -> None:
    parser.add_argument(
        "--network", required=True, help="Name of brownie network to connect to"
    )
    parser.add_argument(
        "--address", required=False, help="Address of deployed contract to connect to"
    )
    if not transact:
        parser.add_argument(
            "--block-number",
            required=False,
            type=int,
            help="Call at the given block number, defaults to latest",
        )
        return
    parser.add_argument(
        "--sender", required=True, help="Path to keystore file for transaction sender"
    )
    parser.add_argument(
        "--password",
        required=False,
        help="Password to keystore file (if you do not provide it, you will be prompted for it)",
    )
    parser.add_argument(
        "--gas-price", default=None, help="Gas price at which to submit transaction"
    )
    parser.add_argument(
        "--max-fee-per-gas",
        default=None,
        help="Max fee per gas for EIP1559 transactions",
    )
    parser.add_argument(
        "--max-priority-fee-per-gas",
        default=None,
        help="Max priority fee per gas for EIP1559 transactions",
    )
    parser.add_argument(
        "--confirmations",
        type=int,
        default=None,
        help="Number of confirmations to await before considering a transaction completed",
    )
    parser.add_argument(
        "--nonce", type=int, default=None, help="Nonce for the transaction (optional)"
    )
    parser.add_argument(
        "--value", default=None, help="Value of the transaction in wei(optional)"
    )
    parser.add_argument("--verbose", action="store_true", help="Print verbose output")


def handle_deploy(args: argparse.Namespace) -> None:
    network.connect(args.network)
    transaction_config = get_transaction_config(args)
    contract = TerminusControllerFacet(None)
    result = contract.deploy(transaction_config=transaction_config)
    print(result)
    if args.verbose:
        print(result.info())


def handle_verify_contract(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = TerminusControllerFacet(args.address)
    result = contract.verify_contract()
    print(result)


def handle_approve_for_pool(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = TerminusControllerFacet(args.address)
    transaction_config = get_transaction_config(args)
    result = contract.approve_for_pool(
        pool_id=args.pool_id,
        operator=args.operator,
        transaction_config=transaction_config,
    )
    print(result)
    if args.verbose:
        print(result.info())


def handle_balance_of(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = TerminusControllerFacet(args.address)
    result = contract.balance_of(
        account=args.account, id=args.id, block_number=args.block_number
    )
    print(result)


def handle_burn(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = TerminusControllerFacet(args.address)
    transaction_config = get_transaction_config(args)
    result = contract.burn(
        from_=args.from_arg,
        pool_id=args.pool_id,
        amount=args.amount,
        transaction_config=transaction_config,
    )
    print(result)
    if args.verbose:
        print(result.info())


def handle_contract_uri(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = TerminusControllerFacet(args.address)
    result = contract.contract_uri(block_number=args.block_number)
    print(result)


def handle_create_pool_v1(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = TerminusControllerFacet(args.address)
    transaction_config = get_transaction_config(args)
    result = contract.create_pool_v1(
        _capacity=args.capacity_arg,
        _transferable=args.transferable_arg,
        _burnable=args.burnable_arg,
        transaction_config=transaction_config,
    )
    print(result)
    if args.verbose:
        print(result.info())


def handle_create_simple_pool(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = TerminusControllerFacet(args.address)
    transaction_config = get_transaction_config(args)
    result = contract.create_simple_pool(
        _capacity=args.capacity_arg, transaction_config=transaction_config
    )
    print(result)
    if args.verbose:
        print(result.info())


def handle_drain_erc1155(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = TerminusControllerFacet(args.address)
    transaction_config = get_transaction_config(args)
    result = contract.drain_erc1155(
        token_address=args.token_address,
        token_id=args.token_id,
        receiver_address=args.receiver_address,
        transaction_config=transaction_config,
    )
    print(result)
    if args.verbose:
        print(result.info())


def handle_drain_erc20(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = TerminusControllerFacet(args.address)
    transaction_config = get_transaction_config(args)
    result = contract.drain_erc20(
        token_address=args.token_address,
        receiver_address=args.receiver_address,
        transaction_config=transaction_config,
    )
    print(result)
    if args.verbose:
        print(result.info())


def handle_get_terminus_address(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = TerminusControllerFacet(args.address)
    result = contract.get_terminus_address(block_number=args.block_number)
    print(result)


def handle_get_terminus_main_admin_pool_id(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = TerminusControllerFacet(args.address)
    result = contract.get_terminus_main_admin_pool_id(block_number=args.block_number)
    print(result)


def handle_get_terminus_pool_controller_pool(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = TerminusControllerFacet(args.address)
    result = contract.get_terminus_pool_controller_pool(
        pool_id=args.pool_id, block_number=args.block_number
    )
    print(result)


def handle_init_terminus_controller(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = TerminusControllerFacet(args.address)
    transaction_config = get_transaction_config(args)
    result = contract.init_terminus_controller(
        terminus_address=args.terminus_address,
        _terminus_main_admin_pool_terminus_address=args.terminus_main_admin_pool_terminus_address_arg,
        _terminus_main_admin_pool_id=args.terminus_main_admin_pool_id_arg,
        transaction_config=transaction_config,
    )
    print(result)
    if args.verbose:
        print(result.info())


def handle_is_approved_for_pool(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = TerminusControllerFacet(args.address)
    result = contract.is_approved_for_pool(
        pool_id=args.pool_id, operator=args.operator, block_number=args.block_number
    )
    print(result)


def handle_mint(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = TerminusControllerFacet(args.address)
    transaction_config = get_transaction_config(args)
    result = contract.mint(
        to=args.to,
        pool_id=args.pool_id,
        amount=args.amount,
        data=args.data,
        transaction_config=transaction_config,
    )
    print(result)
    if args.verbose:
        print(result.info())


def handle_mint_batch(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = TerminusControllerFacet(args.address)
    transaction_config = get_transaction_config(args)
    result = contract.mint_batch(
        to=args.to,
        pool_i_ds=args.pool_i_ds,
        amounts=args.amounts,
        data=args.data,
        transaction_config=transaction_config,
    )
    print(result)
    if args.verbose:
        print(result.info())


def handle_pool_mint_batch(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = TerminusControllerFacet(args.address)
    transaction_config = get_transaction_config(args)
    result = contract.pool_mint_batch(
        id=args.id,
        to_addresses=args.to_addresses,
        amounts=args.amounts,
        transaction_config=transaction_config,
    )
    print(result)
    if args.verbose:
        print(result.info())


def handle_set_contract_uri(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = TerminusControllerFacet(args.address)
    transaction_config = get_transaction_config(args)
    result = contract.set_contract_uri(
        _contract_uri=args.contract_uri_arg, transaction_config=transaction_config
    )
    print(result)
    if args.verbose:
        print(result.info())


def handle_set_controller(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = TerminusControllerFacet(args.address)
    transaction_config = get_transaction_config(args)
    result = contract.set_controller(
        new_controller=args.new_controller, transaction_config=transaction_config
    )
    print(result)
    if args.verbose:
        print(result.info())


def handle_set_pool_control_permissions(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = TerminusControllerFacet(args.address)
    transaction_config = get_transaction_config(args)
    result = contract.set_pool_control_permissions(
        pool_id=args.pool_id,
        terminus_address=args.terminus_address,
        pool_controller_pool_id=args.pool_controller_pool_id,
        transaction_config=transaction_config,
    )
    print(result)
    if args.verbose:
        print(result.info())


def handle_set_pool_controller(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = TerminusControllerFacet(args.address)
    transaction_config = get_transaction_config(args)
    result = contract.set_pool_controller(
        pool_id=args.pool_id,
        new_controller=args.new_controller,
        transaction_config=transaction_config,
    )
    print(result)
    if args.verbose:
        print(result.info())


def handle_set_uri(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = TerminusControllerFacet(args.address)
    transaction_config = get_transaction_config(args)
    result = contract.set_uri(
        pool_id=args.pool_id,
        pool_uri=args.pool_uri,
        transaction_config=transaction_config,
    )
    print(result)
    if args.verbose:
        print(result.info())


def handle_terminus_controller(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = TerminusControllerFacet(args.address)
    result = contract.terminus_controller(block_number=args.block_number)
    print(result)


def handle_terminus_pool_capacity(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = TerminusControllerFacet(args.address)
    result = contract.terminus_pool_capacity(
        pool_id=args.pool_id, block_number=args.block_number
    )
    print(result)


def handle_terminus_pool_controller(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = TerminusControllerFacet(args.address)
    result = contract.terminus_pool_controller(
        pool_id=args.pool_id, block_number=args.block_number
    )
    print(result)


def handle_terminus_pool_supply(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = TerminusControllerFacet(args.address)
    result = contract.terminus_pool_supply(
        pool_id=args.pool_id, block_number=args.block_number
    )
    print(result)


def handle_total_pools(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = TerminusControllerFacet(args.address)
    result = contract.total_pools(block_number=args.block_number)
    print(result)


def handle_unapprove_for_pool(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = TerminusControllerFacet(args.address)
    transaction_config = get_transaction_config(args)
    result = contract.unapprove_for_pool(
        pool_id=args.pool_id,
        operator=args.operator,
        transaction_config=transaction_config,
    )
    print(result)
    if args.verbose:
        print(result.info())


def handle_withdraw_erc1155(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = TerminusControllerFacet(args.address)
    transaction_config = get_transaction_config(args)
    result = contract.withdraw_erc1155(
        token_address=args.token_address,
        token_id=args.token_id,
        amount=args.amount,
        receiver_address=args.receiver_address,
        transaction_config=transaction_config,
    )
    print(result)
    if args.verbose:
        print(result.info())


def handle_withdraw_erc20(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = TerminusControllerFacet(args.address)
    transaction_config = get_transaction_config(args)
    result = contract.withdraw_erc20(
        token_address=args.token_address,
        amount=args.amount,
        receiver_address=args.receiver_address,
        transaction_config=transaction_config,
    )
    print(result)
    if args.verbose:
        print(result.info())


def generate_cli() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="CLI for TerminusControllerFacet")
    parser.set_defaults(func=lambda _: parser.print_help())
    subcommands = parser.add_subparsers()

    deploy_parser = subcommands.add_parser("deploy")
    add_default_arguments(deploy_parser, True)
    deploy_parser.set_defaults(func=handle_deploy)

    verify_contract_parser = subcommands.add_parser("verify-contract")
    add_default_arguments(verify_contract_parser, False)
    verify_contract_parser.set_defaults(func=handle_verify_contract)

    approve_for_pool_parser = subcommands.add_parser("approve-for-pool")
    add_default_arguments(approve_for_pool_parser, True)
    approve_for_pool_parser.add_argument(
        "--pool-id", required=True, help="Type: uint256", type=int
    )
    approve_for_pool_parser.add_argument(
        "--operator", required=True, help="Type: address"
    )
    approve_for_pool_parser.set_defaults(func=handle_approve_for_pool)

    balance_of_parser = subcommands.add_parser("balance-of")
    add_default_arguments(balance_of_parser, False)
    balance_of_parser.add_argument("--account", required=True, help="Type: address")
    balance_of_parser.add_argument(
        "--id", required=True, help="Type: uint256", type=int
    )
    balance_of_parser.set_defaults(func=handle_balance_of)

    burn_parser = subcommands.add_parser("burn")
    add_default_arguments(burn_parser, True)
    burn_parser.add_argument("--from-arg", required=True, help="Type: address")
    burn_parser.add_argument("--pool-id", required=True, help="Type: uint256", type=int)
    burn_parser.add_argument("--amount", required=True, help="Type: uint256", type=int)
    burn_parser.set_defaults(func=handle_burn)

    contract_uri_parser = subcommands.add_parser("contract-uri")
    add_default_arguments(contract_uri_parser, False)
    contract_uri_parser.set_defaults(func=handle_contract_uri)

    create_pool_v1_parser = subcommands.add_parser("create-pool-v1")
    add_default_arguments(create_pool_v1_parser, True)
    create_pool_v1_parser.add_argument(
        "--capacity-arg", required=True, help="Type: uint256", type=int
    )
    create_pool_v1_parser.add_argument(
        "--transferable-arg",
        required=True,
        help="Type: bool",
        type=boolean_argument_type,
    )
    create_pool_v1_parser.add_argument(
        "--burnable-arg", required=True, help="Type: bool", type=boolean_argument_type
    )
    create_pool_v1_parser.set_defaults(func=handle_create_pool_v1)

    create_simple_pool_parser = subcommands.add_parser("create-simple-pool")
    add_default_arguments(create_simple_pool_parser, True)
    create_simple_pool_parser.add_argument(
        "--capacity-arg", required=True, help="Type: uint256", type=int
    )
    create_simple_pool_parser.set_defaults(func=handle_create_simple_pool)

    drain_erc1155_parser = subcommands.add_parser("drain-erc1155")
    add_default_arguments(drain_erc1155_parser, True)
    drain_erc1155_parser.add_argument(
        "--token-address", required=True, help="Type: address"
    )
    drain_erc1155_parser.add_argument(
        "--token-id", required=True, help="Type: uint256", type=int
    )
    drain_erc1155_parser.add_argument(
        "--receiver-address", required=True, help="Type: address"
    )
    drain_erc1155_parser.set_defaults(func=handle_drain_erc1155)

    drain_erc20_parser = subcommands.add_parser("drain-erc20")
    add_default_arguments(drain_erc20_parser, True)
    drain_erc20_parser.add_argument(
        "--token-address", required=True, help="Type: address"
    )
    drain_erc20_parser.add_argument(
        "--receiver-address", required=True, help="Type: address"
    )
    drain_erc20_parser.set_defaults(func=handle_drain_erc20)

    get_terminus_address_parser = subcommands.add_parser("get-terminus-address")
    add_default_arguments(get_terminus_address_parser, False)
    get_terminus_address_parser.set_defaults(func=handle_get_terminus_address)

    get_terminus_main_admin_pool_id_parser = subcommands.add_parser(
        "get-terminus-main-admin-pool-id"
    )
    add_default_arguments(get_terminus_main_admin_pool_id_parser, False)
    get_terminus_main_admin_pool_id_parser.set_defaults(
        func=handle_get_terminus_main_admin_pool_id
    )

    get_terminus_pool_controller_pool_parser = subcommands.add_parser(
        "get-terminus-pool-controller-pool"
    )
    add_default_arguments(get_terminus_pool_controller_pool_parser, False)
    get_terminus_pool_controller_pool_parser.add_argument(
        "--pool-id", required=True, help="Type: uint256", type=int
    )
    get_terminus_pool_controller_pool_parser.set_defaults(
        func=handle_get_terminus_pool_controller_pool
    )

    init_terminus_controller_parser = subcommands.add_parser("init-terminus-controller")
    add_default_arguments(init_terminus_controller_parser, True)
    init_terminus_controller_parser.add_argument(
        "--terminus-address", required=True, help="Type: address"
    )
    init_terminus_controller_parser.add_argument(
        "--terminus-main-admin-pool-terminus-address-arg",
        required=True,
        help="Type: address",
    )
    init_terminus_controller_parser.add_argument(
        "--terminus-main-admin-pool-id-arg",
        required=True,
        help="Type: uint256",
        type=int,
    )
    init_terminus_controller_parser.set_defaults(func=handle_init_terminus_controller)

    is_approved_for_pool_parser = subcommands.add_parser("is-approved-for-pool")
    add_default_arguments(is_approved_for_pool_parser, False)
    is_approved_for_pool_parser.add_argument(
        "--pool-id", required=True, help="Type: uint256", type=int
    )
    is_approved_for_pool_parser.add_argument(
        "--operator", required=True, help="Type: address"
    )
    is_approved_for_pool_parser.set_defaults(func=handle_is_approved_for_pool)

    mint_parser = subcommands.add_parser("mint")
    add_default_arguments(mint_parser, True)
    mint_parser.add_argument("--to", required=True, help="Type: address")
    mint_parser.add_argument("--pool-id", required=True, help="Type: uint256", type=int)
    mint_parser.add_argument("--amount", required=True, help="Type: uint256", type=int)
    mint_parser.add_argument(
        "--data", required=True, help="Type: bytes", type=bytes_argument_type
    )
    mint_parser.set_defaults(func=handle_mint)

    mint_batch_parser = subcommands.add_parser("mint-batch")
    add_default_arguments(mint_batch_parser, True)
    mint_batch_parser.add_argument("--to", required=True, help="Type: address")
    mint_batch_parser.add_argument(
        "--pool-i-ds", required=True, help="Type: uint256[]", nargs="+"
    )
    mint_batch_parser.add_argument(
        "--amounts", required=True, help="Type: uint256[]", nargs="+"
    )
    mint_batch_parser.add_argument(
        "--data", required=True, help="Type: bytes", type=bytes_argument_type
    )
    mint_batch_parser.set_defaults(func=handle_mint_batch)

    pool_mint_batch_parser = subcommands.add_parser("pool-mint-batch")
    add_default_arguments(pool_mint_batch_parser, True)
    pool_mint_batch_parser.add_argument(
        "--id", required=True, help="Type: uint256", type=int
    )
    pool_mint_batch_parser.add_argument(
        "--to-addresses", required=True, help="Type: address[]", nargs="+"
    )
    pool_mint_batch_parser.add_argument(
        "--amounts", required=True, help="Type: uint256[]", nargs="+"
    )
    pool_mint_batch_parser.set_defaults(func=handle_pool_mint_batch)

    set_contract_uri_parser = subcommands.add_parser("set-contract-uri")
    add_default_arguments(set_contract_uri_parser, True)
    set_contract_uri_parser.add_argument(
        "--contract-uri-arg", required=True, help="Type: string", type=str
    )
    set_contract_uri_parser.set_defaults(func=handle_set_contract_uri)

    set_controller_parser = subcommands.add_parser("set-controller")
    add_default_arguments(set_controller_parser, True)
    set_controller_parser.add_argument(
        "--new-controller", required=True, help="Type: address"
    )
    set_controller_parser.set_defaults(func=handle_set_controller)

    set_pool_control_permissions_parser = subcommands.add_parser(
        "set-pool-control-permissions"
    )
    add_default_arguments(set_pool_control_permissions_parser, True)
    set_pool_control_permissions_parser.add_argument(
        "--pool-id", required=True, help="Type: uint256", type=int
    )
    set_pool_control_permissions_parser.add_argument(
        "--terminus-address", required=True, help="Type: address"
    )
    set_pool_control_permissions_parser.add_argument(
        "--pool-controller-pool-id", required=True, help="Type: uint256", type=int
    )
    set_pool_control_permissions_parser.set_defaults(
        func=handle_set_pool_control_permissions
    )

    set_pool_controller_parser = subcommands.add_parser("set-pool-controller")
    add_default_arguments(set_pool_controller_parser, True)
    set_pool_controller_parser.add_argument(
        "--pool-id", required=True, help="Type: uint256", type=int
    )
    set_pool_controller_parser.add_argument(
        "--new-controller", required=True, help="Type: address"
    )
    set_pool_controller_parser.set_defaults(func=handle_set_pool_controller)

    set_uri_parser = subcommands.add_parser("set-uri")
    add_default_arguments(set_uri_parser, True)
    set_uri_parser.add_argument(
        "--pool-id", required=True, help="Type: uint256", type=int
    )
    set_uri_parser.add_argument(
        "--pool-uri", required=True, help="Type: string", type=str
    )
    set_uri_parser.set_defaults(func=handle_set_uri)

    terminus_controller_parser = subcommands.add_parser("terminus-controller")
    add_default_arguments(terminus_controller_parser, False)
    terminus_controller_parser.set_defaults(func=handle_terminus_controller)

    terminus_pool_capacity_parser = subcommands.add_parser("terminus-pool-capacity")
    add_default_arguments(terminus_pool_capacity_parser, False)
    terminus_pool_capacity_parser.add_argument(
        "--pool-id", required=True, help="Type: uint256", type=int
    )
    terminus_pool_capacity_parser.set_defaults(func=handle_terminus_pool_capacity)

    terminus_pool_controller_parser = subcommands.add_parser("terminus-pool-controller")
    add_default_arguments(terminus_pool_controller_parser, False)
    terminus_pool_controller_parser.add_argument(
        "--pool-id", required=True, help="Type: uint256", type=int
    )
    terminus_pool_controller_parser.set_defaults(func=handle_terminus_pool_controller)

    terminus_pool_supply_parser = subcommands.add_parser("terminus-pool-supply")
    add_default_arguments(terminus_pool_supply_parser, False)
    terminus_pool_supply_parser.add_argument(
        "--pool-id", required=True, help="Type: uint256", type=int
    )
    terminus_pool_supply_parser.set_defaults(func=handle_terminus_pool_supply)

    total_pools_parser = subcommands.add_parser("total-pools")
    add_default_arguments(total_pools_parser, False)
    total_pools_parser.set_defaults(func=handle_total_pools)

    unapprove_for_pool_parser = subcommands.add_parser("unapprove-for-pool")
    add_default_arguments(unapprove_for_pool_parser, True)
    unapprove_for_pool_parser.add_argument(
        "--pool-id", required=True, help="Type: uint256", type=int
    )
    unapprove_for_pool_parser.add_argument(
        "--operator", required=True, help="Type: address"
    )
    unapprove_for_pool_parser.set_defaults(func=handle_unapprove_for_pool)

    withdraw_erc1155_parser = subcommands.add_parser("withdraw-erc1155")
    add_default_arguments(withdraw_erc1155_parser, True)
    withdraw_erc1155_parser.add_argument(
        "--token-address", required=True, help="Type: address"
    )
    withdraw_erc1155_parser.add_argument(
        "--token-id", required=True, help="Type: uint256", type=int
    )
    withdraw_erc1155_parser.add_argument(
        "--amount", required=True, help="Type: uint256", type=int
    )
    withdraw_erc1155_parser.add_argument(
        "--receiver-address", required=True, help="Type: address"
    )
    withdraw_erc1155_parser.set_defaults(func=handle_withdraw_erc1155)

    withdraw_erc20_parser = subcommands.add_parser("withdraw-erc20")
    add_default_arguments(withdraw_erc20_parser, True)
    withdraw_erc20_parser.add_argument(
        "--token-address", required=True, help="Type: address"
    )
    withdraw_erc20_parser.add_argument(
        "--amount", required=True, help="Type: uint256", type=int
    )
    withdraw_erc20_parser.add_argument(
        "--receiver-address", required=True, help="Type: address"
    )
    withdraw_erc20_parser.set_defaults(func=handle_withdraw_erc20)

    return parser


def main() -> None:
    parser = generate_cli()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
