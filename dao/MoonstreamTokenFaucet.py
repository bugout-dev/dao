# Code generated by moonworm : https://github.com/bugout-dev/moonworm
# Moonworm version : 0.1.16

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


def bytes_argument_type(raw_value: str) -> bytes:
    return raw_value.encode()


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


class MoonstreamTokenFaucet:
    def __init__(self, contract_address: Optional[ChecksumAddress]):
        self.contract_name = "MoonstreamTokenFaucet"
        self.address = contract_address
        self.contract = None
        self.abi = get_abi_json("MoonstreamTokenFaucet")
        if self.address is not None:
            self.contract: Optional[Contract] = Contract.from_abi(
                self.contract_name, self.address, self.abi
            )

    def deploy(
        self,
        _moonstream_token_address: ChecksumAddress,
        owner: ChecksumAddress,
        _faucet_amount: int,
        _faucet_block_interval: int,
        transaction_config,
    ):
        contract_class = contract_from_build(self.contract_name)
        deployed_contract = contract_class.deploy(
            _moonstream_token_address,
            owner,
            _faucet_amount,
            _faucet_block_interval,
            transaction_config,
        )
        self.address = deployed_contract.address
        self.contract = deployed_contract

    def assert_contract_is_instantiated(self) -> None:
        if self.contract is None:
            raise Exception("contract has not been instantiated")

    def verify_contract(self):
        self.assert_contract_is_instantiated()
        contract_class = contract_from_build(self.contract_name)
        contract_class.publish_source(self.contract)

    def claim(self, transaction_config) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.claim(transaction_config)

    def get_faucet_amount(self) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.getFaucetAmount.call()

    def get_faucet_block_interval(self) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.getFaucetBlockInterval.call()

    def get_last_claimed_block(self, _address: ChecksumAddress) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.getLastClaimedBlock.call(_address)

    def get_moonstream_token_address(self) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.getMoonstreamTokenAddress.call()

    def get_moonstream_token_balance(self, _address: ChecksumAddress) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.getMoonstreamTokenBalance.call(_address)

    def owner(self) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.owner.call()

    def renounce_ownership(self, transaction_config) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.renounceOwnership(transaction_config)

    def set_faucet_amount(self, _faucet_amount: int, transaction_config) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.setFaucetAmount(_faucet_amount, transaction_config)

    def set_faucet_block_interval(
        self, _faucet_block_interval: int, transaction_config
    ) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.setFaucetBlockInterval(
            _faucet_block_interval, transaction_config
        )

    def set_moonstream_token_address(
        self, _moonstream_token_address: ChecksumAddress, transaction_config
    ) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.setMoonstreamTokenAddress(
            _moonstream_token_address, transaction_config
        )

    def transfer_ownership(self, new_owner: ChecksumAddress, transaction_config) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.transferOwnership(new_owner, transaction_config)


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


def handle_deploy(args: argparse.Namespace) -> None:
    network.connect(args.network)
    transaction_config = get_transaction_config(args)
    contract = MoonstreamTokenFaucet(None)
    result = contract.deploy(
        _moonstream_token_address=args.moonstream_token_address_arg,
        owner=args.owner,
        _faucet_amount=args.faucet_amount_arg,
        _faucet_block_interval=args.faucet_block_interval_arg,
        transaction_config=transaction_config,
    )
    print(result)


def handle_verify_contract(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = MoonstreamTokenFaucet(args.address)
    result = contract.verify_contract()
    print(result)


def handle_claim(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = MoonstreamTokenFaucet(args.address)
    transaction_config = get_transaction_config(args)
    result = contract.claim(transaction_config=transaction_config)
    print(result)


def handle_get_faucet_amount(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = MoonstreamTokenFaucet(args.address)
    result = contract.get_faucet_amount()
    print(result)


def handle_get_faucet_block_interval(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = MoonstreamTokenFaucet(args.address)
    result = contract.get_faucet_block_interval()
    print(result)


def handle_get_last_claimed_block(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = MoonstreamTokenFaucet(args.address)
    result = contract.get_last_claimed_block(_address=args.address_arg)
    print(result)


def handle_get_moonstream_token_address(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = MoonstreamTokenFaucet(args.address)
    result = contract.get_moonstream_token_address()
    print(result)


def handle_get_moonstream_token_balance(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = MoonstreamTokenFaucet(args.address)
    result = contract.get_moonstream_token_balance(_address=args.address_arg)
    print(result)


def handle_owner(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = MoonstreamTokenFaucet(args.address)
    result = contract.owner()
    print(result)


def handle_renounce_ownership(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = MoonstreamTokenFaucet(args.address)
    transaction_config = get_transaction_config(args)
    result = contract.renounce_ownership(transaction_config=transaction_config)
    print(result)


def handle_set_faucet_amount(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = MoonstreamTokenFaucet(args.address)
    transaction_config = get_transaction_config(args)
    result = contract.set_faucet_amount(
        _faucet_amount=args.faucet_amount_arg, transaction_config=transaction_config
    )
    print(result)


def handle_set_faucet_block_interval(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = MoonstreamTokenFaucet(args.address)
    transaction_config = get_transaction_config(args)
    result = contract.set_faucet_block_interval(
        _faucet_block_interval=args.faucet_block_interval_arg,
        transaction_config=transaction_config,
    )
    print(result)


def handle_set_moonstream_token_address(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = MoonstreamTokenFaucet(args.address)
    transaction_config = get_transaction_config(args)
    result = contract.set_moonstream_token_address(
        _moonstream_token_address=args.moonstream_token_address_arg,
        transaction_config=transaction_config,
    )
    print(result)


def handle_transfer_ownership(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = MoonstreamTokenFaucet(args.address)
    transaction_config = get_transaction_config(args)
    result = contract.transfer_ownership(
        new_owner=args.new_owner, transaction_config=transaction_config
    )
    print(result)


def generate_cli() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="CLI for MoonstreamTokenFaucet")
    parser.set_defaults(func=lambda _: parser.print_help())
    subcommands = parser.add_subparsers()

    deploy_parser = subcommands.add_parser("deploy")
    add_default_arguments(deploy_parser, True)
    deploy_parser.add_argument(
        "--moonstream-token-address-arg", required=True, help="Type: address"
    )
    deploy_parser.add_argument("--owner", required=True, help="Type: address")
    deploy_parser.add_argument(
        "--faucet-amount-arg", required=True, help="Type: uint256", type=int
    )
    deploy_parser.add_argument(
        "--faucet-block-interval-arg", required=True, help="Type: uint256", type=int
    )
    deploy_parser.set_defaults(func=handle_deploy)

    verify_contract_parser = subcommands.add_parser("verify-contract")
    add_default_arguments(verify_contract_parser, False)
    verify_contract_parser.set_defaults(func=handle_verify_contract)

    claim_parser = subcommands.add_parser("claim")
    add_default_arguments(claim_parser, True)
    claim_parser.set_defaults(func=handle_claim)

    get_faucet_amount_parser = subcommands.add_parser("get-faucet-amount")
    add_default_arguments(get_faucet_amount_parser, False)
    get_faucet_amount_parser.set_defaults(func=handle_get_faucet_amount)

    get_faucet_block_interval_parser = subcommands.add_parser(
        "get-faucet-block-interval"
    )
    add_default_arguments(get_faucet_block_interval_parser, False)
    get_faucet_block_interval_parser.set_defaults(func=handle_get_faucet_block_interval)

    get_last_claimed_block_parser = subcommands.add_parser("get-last-claimed-block")
    add_default_arguments(get_last_claimed_block_parser, False)
    get_last_claimed_block_parser.add_argument(
        "--address-arg", required=True, help="Type: address"
    )
    get_last_claimed_block_parser.set_defaults(func=handle_get_last_claimed_block)

    get_moonstream_token_address_parser = subcommands.add_parser(
        "get-moonstream-token-address"
    )
    add_default_arguments(get_moonstream_token_address_parser, False)
    get_moonstream_token_address_parser.set_defaults(
        func=handle_get_moonstream_token_address
    )

    get_moonstream_token_balance_parser = subcommands.add_parser(
        "get-moonstream-token-balance"
    )
    add_default_arguments(get_moonstream_token_balance_parser, False)
    get_moonstream_token_balance_parser.add_argument(
        "--address-arg", required=True, help="Type: address"
    )
    get_moonstream_token_balance_parser.set_defaults(
        func=handle_get_moonstream_token_balance
    )

    owner_parser = subcommands.add_parser("owner")
    add_default_arguments(owner_parser, False)
    owner_parser.set_defaults(func=handle_owner)

    renounce_ownership_parser = subcommands.add_parser("renounce-ownership")
    add_default_arguments(renounce_ownership_parser, True)
    renounce_ownership_parser.set_defaults(func=handle_renounce_ownership)

    set_faucet_amount_parser = subcommands.add_parser("set-faucet-amount")
    add_default_arguments(set_faucet_amount_parser, True)
    set_faucet_amount_parser.add_argument(
        "--faucet-amount-arg", required=True, help="Type: uint256", type=int
    )
    set_faucet_amount_parser.set_defaults(func=handle_set_faucet_amount)

    set_faucet_block_interval_parser = subcommands.add_parser(
        "set-faucet-block-interval"
    )
    add_default_arguments(set_faucet_block_interval_parser, True)
    set_faucet_block_interval_parser.add_argument(
        "--faucet-block-interval-arg", required=True, help="Type: uint256", type=int
    )
    set_faucet_block_interval_parser.set_defaults(func=handle_set_faucet_block_interval)

    set_moonstream_token_address_parser = subcommands.add_parser(
        "set-moonstream-token-address"
    )
    add_default_arguments(set_moonstream_token_address_parser, True)
    set_moonstream_token_address_parser.add_argument(
        "--moonstream-token-address-arg", required=True, help="Type: address"
    )
    set_moonstream_token_address_parser.set_defaults(
        func=handle_set_moonstream_token_address
    )

    transfer_ownership_parser = subcommands.add_parser("transfer-ownership")
    add_default_arguments(transfer_ownership_parser, True)
    transfer_ownership_parser.add_argument(
        "--new-owner", required=True, help="Type: address"
    )
    transfer_ownership_parser.set_defaults(func=handle_transfer_ownership)

    return parser


def main() -> None:
    parser = generate_cli()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
