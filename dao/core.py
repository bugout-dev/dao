"""
Generic diamond functionality for Moonstream contracts.
"""

import argparse
import json
import os
import sys
from typing import Any, Dict, List, Optional, Set

from brownie import network

from . import (
    abi,
    Diamond,
    DiamondCutFacet,
    DiamondLoupeFacet,
    ERC20Facet,
    ERC20Initializer,
    OwnershipFacet,
    TerminusFacet,
    TerminusInitializer,
)

FACETS: Dict[str, Any] = {
    "DiamondCutFacet": DiamondCutFacet,
    "DiamondLoupeFacet": DiamondLoupeFacet,
    "ERC20Facet": ERC20Facet,
    "OwnershipFacet": OwnershipFacet,
    "TerminusFacet": TerminusFacet,
}

FACET_PRECEDENCE: List[str] = [
    "DiamondCutFacet",
    "OwnershipFacet",
    "DiamondLoupeFacet",
    "ERC20Facet",
    "TerminusFacet",
]

FACET_ACTIONS: Dict[str, int] = {"add": 0, "replace": 1, "remove": 2}

ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"


def facet_cut(
    diamond_address: str,
    facet_name: str,
    facet_address: str,
    action: str,
    transaction_config: Dict[str, Any],
    initializer_address: str = ZERO_ADDRESS,
    ignore_methods: Optional[List[str]] = None,
    ignore_selectors: Optional[List[str]] = None,
    methods: Optional[List[str]] = None,
    selectors: Optional[List[str]] = None,
    initializer_params: Optional[List[Any]] = None,
) -> Any:
    """
    Cuts the given facet onto the given Diamond contract.

    Resolves selectors in the precedence order defined by FACET_PRECEDENCE (highest precedence first).
    """
    assert (
        facet_name in FACETS
    ), f"Invalid facet: {facet_name}. Choices: {','.join(FACETS)}."

    assert (
        action in FACET_ACTIONS
    ), f"Invalid cut action: {action}. Choices: {','.join(FACET_ACTIONS)}."

    if ignore_methods is None:
        ignore_methods = []
    if ignore_selectors is None:
        ignore_selectors = []
    if methods is None:
        methods = []
    if selectors is None:
        selectors = []

    project_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    abis = abi.project_abis(project_dir)

    reserved_selectors: Set[str] = set()
    for facet in FACET_PRECEDENCE:
        if facet == facet_name:
            break

        facet_abi = abis.get(facet, [])
        for item in facet_abi:
            if item["type"] == "function":
                reserved_selectors.add(abi.encode_function_signature(item))

    facet_function_selectors: List[str] = []
    facet_abi = abis.get(facet_name, [])

    logical_operator = all
    method_predicate = lambda method: method not in ignore_methods
    selector_predicate = (
        lambda selector: selector not in reserved_selectors
        and selector not in ignore_selectors
    )

    if len(methods) > 0 or len(selectors) > 0:
        logical_operator = any
        method_predicate = lambda method: method in methods
        selector_predicate = lambda selector: selector in selectors

    for item in facet_abi:
        if item["type"] == "function":
            item_selector = abi.encode_function_signature(item)
            if logical_operator(
                [method_predicate(item["name"]), selector_predicate(item_selector)]
            ):
                facet_function_selectors.append(item_selector)

    target_address = facet_address
    if FACET_ACTIONS[action] == 2:
        target_address = ZERO_ADDRESS

    diamond_cut_action = [
        target_address,
        FACET_ACTIONS[action],
        facet_function_selectors,
    ]

    calldata = b""
    if facet_name == "ERC20Facet":
        if initializer_address != ZERO_ADDRESS and action != "remove":
            erc20_initializer = ERC20Initializer.ERC20Initializer(initializer_address)
            calldata = erc20_initializer.contract.init.encode_input(
                initializer_params[0], initializer_params[1]
            )
    elif facet_name == "TerminusFacet":
        if initializer_address != ZERO_ADDRESS and action != "remove":
            terminus_initializer = TerminusInitializer.TerminusInitializer(
                initializer_address
            )
            calldata = terminus_initializer.contract.init.encode_input()

    diamond = DiamondCutFacet.DiamondCutFacet(diamond_address)
    transaction = diamond.diamond_cut(
        [diamond_cut_action], initializer_address, calldata, transaction_config
    )
    return transaction


def gogogo(owner_address: str, transaction_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Deploy diamond along with all its basic facets and attach those facets to the diamond.

    Returns addresses of all the deployed contracts with the contract names as keys.
    """
    result: Dict[str, Any] = {}

    try:
        diamond_cut_facet = DiamondCutFacet.DiamondCutFacet(None)
        diamond_cut_facet.deploy(transaction_config)
    except Exception as e:
        print(e)
        result["error"] = "Failed to deploy DiamondCutFacet"
        return result
    result["DiamondCutFacet"] = diamond_cut_facet.address

    try:
        diamond = Diamond.Diamond(None)
        diamond.deploy(owner_address, diamond_cut_facet.address, transaction_config)
    except Exception as e:
        print(e)
        result["error"] = "Failed to deploy Diamond"
        return result
    result["Diamond"] = diamond.address

    try:
        diamond_loupe_facet = DiamondLoupeFacet.DiamondLoupeFacet(None)
        diamond_loupe_facet.deploy(transaction_config)
    except Exception as e:
        print(e)
        result["error"] = "Failed to deploy DiamondLoupeFacet"
        return result
    result["DiamondLoupeFacet"] = diamond_loupe_facet.address

    try:
        ownership_facet = OwnershipFacet.OwnershipFacet(None)
        ownership_facet.deploy(transaction_config)
    except Exception as e:
        print(e)
        result["error"] = "Failed to deploy OwnershipFacet"
        return result
    result["OwnershipFacet"] = ownership_facet.address

    result["attached"] = []

    try:
        facet_cut(
            diamond.address,
            "DiamondLoupeFacet",
            diamond_loupe_facet.address,
            "add",
            transaction_config,
        )
    except Exception as e:
        print(e)
        result["error"] = "Failed to attach DiamondLoupeFacet"
        return result
    result["attached"].append("DiamondLoupeFacet")

    try:
        facet_cut(
            diamond.address,
            "OwnershipFacet",
            ownership_facet.address,
            "add",
            transaction_config,
        )
    except Exception as e:
        print(e)
        result["error"] = "Failed to attach OwnershipFacet"
        return result
    result["attached"].append("OwnershipFacet")

    return result


def handle_facet_cut(args: argparse.Namespace) -> None:
    network.connect(args.network)
    diamond_address = args.address
    action = args.action
    facet_name = args.facet_name
    facet_address = args.facet_address
    transaction_config = Diamond.get_transaction_config(args)
    facet_cut(
        diamond_address,
        facet_name,
        facet_address,
        action,
        transaction_config,
        initializer_address=args.initializer_address,
        ignore_methods=args.ignore_methods,
        ignore_selectors=args.ignore_selectors,
        methods=args.methods,
        selectors=args.selectors,
    )


def handle_gogogo(args: argparse.Namespace) -> None:
    network.connect(args.network)
    owner_address = args.owner
    transaction_config = Diamond.get_transaction_config(args)
    result = gogogo(owner_address, transaction_config)
    if args.outfile is not None:
        with args.outfile:
            json.dump(result, args.outfile)
    json.dump(result, sys.stdout, indent=4)


def generate_cli() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="CLI to manage Moonstream DAO diamond contracts",
    )
    parser.set_defaults(func=lambda _: parser.print_help())
    subcommands = parser.add_subparsers()

    Diamond_parser = Diamond.generate_cli()
    subcommands.add_parser("diamond", parents=[Diamond_parser], add_help=False)

    facet_cut_parser = subcommands.add_parser("facet-cut")
    Diamond.add_default_arguments(facet_cut_parser, transact=True)
    facet_cut_parser.add_argument(
        "--facet-name",
        required=True,
        choices=FACETS,
        help="Name of facet to cut into or out of diamond",
    )
    facet_cut_parser.add_argument(
        "--facet-address",
        required=False,
        default=ZERO_ADDRESS,
        help=f"Address of deployed facet (default: {ZERO_ADDRESS})",
    )
    facet_cut_parser.add_argument(
        "--action",
        required=True,
        choices=FACET_ACTIONS,
        help="Diamond cut action to take on entire facet",
    )
    facet_cut_parser.add_argument(
        "--initializer-address",
        default=ZERO_ADDRESS,
        help=f"Address of contract to run as initializer after cut (default: {ZERO_ADDRESS})",
    )
    facet_cut_parser.add_argument(
        "--ignore-methods",
        nargs="+",
        help="Names of methods to ignore when cutting a facet onto or off of the diamond",
    )
    facet_cut_parser.add_argument(
        "--ignore-selectors",
        nargs="+",
        help="Method selectors to ignore when cutting a facet onto or off of the diamond",
    )
    facet_cut_parser.add_argument(
        "--methods",
        nargs="+",
        help="Names of methods to add (if set, --ignore-methods and --ignore-selectors are not used)",
    )
    facet_cut_parser.add_argument(
        "--selectors",
        nargs="+",
        help="Selectors to add (if set, --ignore-methods and --ignore-selectors are not used)",
    )
    facet_cut_parser.set_defaults(func=handle_facet_cut)

    gogogo_parser = subcommands.add_parser("gogogo")
    Diamond.add_default_arguments(gogogo_parser, transact=True)
    gogogo_parser.add_argument(
        "--owner", required=True, help="Address of owner of diamond proxy"
    )
    gogogo_parser.add_argument(
        "-o",
        "--outfile",
        type=argparse.FileType("w"),
        default=None,
        help="(Optional) file to write deployed addresses to",
    )
    gogogo_parser.set_defaults(func=handle_gogogo)

    DiamondCutFacet_parser = DiamondCutFacet.generate_cli()
    subcommands.add_parser(
        "diamond-cut", parents=[DiamondCutFacet_parser], add_help=False
    )

    DiamondLoupeFacet_parser = DiamondLoupeFacet.generate_cli()
    subcommands.add_parser(
        "diamond-loupe", parents=[DiamondLoupeFacet_parser], add_help=False
    )

    OwnershipFacet_parser = OwnershipFacet.generate_cli()
    subcommands.add_parser("ownership", parents=[OwnershipFacet_parser], add_help=False)

    return parser


def main() -> None:
    parser = generate_cli()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
