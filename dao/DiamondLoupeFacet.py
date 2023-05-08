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


class DiamondLoupeFacet:
    def __init__(self, contract_address: Optional[ChecksumAddress]):
        self.contract_name = "DiamondLoupeFacet"
        self.address = contract_address
        self.contract = None
        self.abi = get_abi_json("DiamondLoupeFacet")
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

    def facet_address(
        self,
        _function_selector: bytes,
        block_number: Optional[Union[str, int]] = "latest",
    ) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.facetAddress.call(
            _function_selector, block_identifier=block_number
        )

    def facet_addresses(
        self, block_number: Optional[Union[str, int]] = "latest"
    ) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.facetAddresses.call(block_identifier=block_number)

    def facet_function_selectors(
        self,
        _facet: ChecksumAddress,
        block_number: Optional[Union[str, int]] = "latest",
    ) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.facetFunctionSelectors.call(
            _facet, block_identifier=block_number
        )

    def facets(self, block_number: Optional[Union[str, int]] = "latest") -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.facets.call(block_identifier=block_number)

    def supports_interface(
        self, _interface_id: bytes, block_number: Optional[Union[str, int]] = "latest"
    ) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.supportsInterface.call(
            _interface_id, block_identifier=block_number
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
    contract = DiamondLoupeFacet(None)
    result = contract.deploy(transaction_config=transaction_config)
    print(result)
    if args.verbose:
        print(result.info())


def handle_verify_contract(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = DiamondLoupeFacet(args.address)
    result = contract.verify_contract()
    print(result)


def handle_facet_address(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = DiamondLoupeFacet(args.address)
    result = contract.facet_address(
        _function_selector=args.function_selector_arg, block_number=args.block_number
    )
    print(result)


def handle_facet_addresses(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = DiamondLoupeFacet(args.address)
    result = contract.facet_addresses(block_number=args.block_number)
    print(result)


def handle_facet_function_selectors(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = DiamondLoupeFacet(args.address)
    result = contract.facet_function_selectors(
        _facet=args.facet_arg, block_number=args.block_number
    )
    print(result)


def handle_facets(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = DiamondLoupeFacet(args.address)
    result = contract.facets(block_number=args.block_number)
    print(result)


def handle_supports_interface(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = DiamondLoupeFacet(args.address)
    result = contract.supports_interface(
        _interface_id=args.interface_id_arg, block_number=args.block_number
    )
    print(result)


def generate_cli() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="CLI for DiamondLoupeFacet")
    parser.set_defaults(func=lambda _: parser.print_help())
    subcommands = parser.add_subparsers()

    deploy_parser = subcommands.add_parser("deploy")
    add_default_arguments(deploy_parser, True)
    deploy_parser.set_defaults(func=handle_deploy)

    verify_contract_parser = subcommands.add_parser("verify-contract")
    add_default_arguments(verify_contract_parser, False)
    verify_contract_parser.set_defaults(func=handle_verify_contract)

    facet_address_parser = subcommands.add_parser("facet-address")
    add_default_arguments(facet_address_parser, False)
    facet_address_parser.add_argument(
        "--function-selector-arg",
        required=True,
        help="Type: bytes4",
        type=bytes_argument_type,
    )
    facet_address_parser.set_defaults(func=handle_facet_address)

    facet_addresses_parser = subcommands.add_parser("facet-addresses")
    add_default_arguments(facet_addresses_parser, False)
    facet_addresses_parser.set_defaults(func=handle_facet_addresses)

    facet_function_selectors_parser = subcommands.add_parser("facet-function-selectors")
    add_default_arguments(facet_function_selectors_parser, False)
    facet_function_selectors_parser.add_argument(
        "--facet-arg", required=True, help="Type: address"
    )
    facet_function_selectors_parser.set_defaults(func=handle_facet_function_selectors)

    facets_parser = subcommands.add_parser("facets")
    add_default_arguments(facets_parser, False)
    facets_parser.set_defaults(func=handle_facets)

    supports_interface_parser = subcommands.add_parser("supports-interface")
    add_default_arguments(supports_interface_parser, False)
    supports_interface_parser.add_argument(
        "--interface-id-arg",
        required=True,
        help="Type: bytes4",
        type=bytes_argument_type,
    )
    supports_interface_parser.set_defaults(func=handle_supports_interface)

    return parser


def main() -> None:
    parser = generate_cli()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
