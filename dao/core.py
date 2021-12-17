"""
Generic diamond functionality for Moonstream contracts.
"""

import argparse
import os
from typing import Any, Dict, List, Optional, Set

from brownie import network

from . import (
    abi,
    Diamond,
    DiamondCutFacet,
    DiamondLoupeFacet,
    ERC20Facet,
    OwnershipFacet,
)

FACETS: Dict[str, Any] = {
    "DiamondCutFacet": DiamondCutFacet,
    "DiamondLoupeFacet": DiamondLoupeFacet,
    "ERC20Facet": ERC20Facet,
    "OwnershipFacet": OwnershipFacet,
}

FACET_PRECEDENCE: List[str] = [
    "DiamondCutFacet",
    "OwnershipFacet",
    "DiamondLoupeFacet",
    "ERC20Facet",
]

FACET_ACTIONS: Dict[str, int] = {"add": 0, "replace": 1, "remove": 2}

ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"


def facet_cut(
    diamond_address: str,
    facet_name: str,
    facet_address: str,
    action: str,
    transaction_config: Dict[str, Any],
    ignore_methods: Optional[List[str]] = None,
    ignore_selectors: Optional[List[str]] = None,
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
    for item in facet_abi:
        if item["type"] == "function":
            if item["name"] not in ignore_methods:
                function_selector = abi.encode_function_signature(item)
                if (
                    function_selector not in reserved_selectors
                    and function_selector not in ignore_selectors
                ):
                    facet_function_selectors.append(function_selector)

    target_address = facet_address
    if FACET_ACTIONS[action] == 2:
        target_address = ZERO_ADDRESS

    diamond_cut_action = [
        target_address,
        FACET_ACTIONS[action],
        facet_function_selectors,
    ]

    diamond = DiamondCutFacet.DiamondCutFacet(diamond_address)
    transaction = diamond.diamond_cut(
        [diamond_cut_action], ZERO_ADDRESS, b"", transaction_config
    )
    return transaction


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
        ignore_methods=args.ignore_methods,
        ignore_selectors=args.ignore_selectors,
    )


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
        "--ignore-methods",
        nargs="+",
        help="Names of methods to ignore when cutting a facet onto or off of the diamond",
    )
    facet_cut_parser.add_argument(
        "--ignore-selectors",
        nargs="+",
        help="Method selectors to ignore when cutting a facet onto or off of the diamond",
    )
    facet_cut_parser.set_defaults(func=handle_facet_cut)

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
