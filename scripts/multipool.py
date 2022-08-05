"""
Operations on multiple pools
"""

import argparse

from brownie import network

from dao import TerminusFacet


def add_positional_pool_ids_arg(command_parser: argparse.ArgumentParser) -> None:
    command_parser.add_argument(
        "pools",
        nargs="+",
        help="List of pool IDs for which to perform these operations",
    )


def handle_pool_controllers(args: argparse.Namespace) -> None:
    network.connect(args.network)
    terminus = TerminusFacet.TerminusFacet(args.address)
    for pool_id in args.pools:
        controller = terminus.terminus_pool_controller(pool_id, args.block_number)
        print(f"Pool ID: {pool_id}, controller: {controller}")


def handle_balance_of(args: argparse.Namespace) -> None:
    network.connect(args.network)
    terminus = TerminusFacet.TerminusFacet(args.address)
    print(f"Balances for owner: {args.owner}")
    balances = terminus.balance_of_batch(
        [args.owner] * len(args.pools), args.pools, args.block_number
    )
    for pool_id, balance in zip(args.pools, balances):
        print(f"- Pool ID: {pool_id}, balance: {balance}")


def handle_is_approved_for_pools(args: argparse.Namespace) -> None:
    network.connect(args.network)
    terminus = TerminusFacet.TerminusFacet(args.address)
    print(f"Pool approvals for operator: {args.operator}")
    for pool_id in args.pools:
        is_approved = terminus.is_approved_for_pool(
            pool_id, args.operator, args.block_number
        )
        print(f"Pool ID: {pool_id}, approved: {is_approved}")


def handle_approve_for_pools(args: argparse.Namespace) -> None:
    network.connect(args.network)
    transaction_config = TerminusFacet.get_transaction_config(args)

    terminus = TerminusFacet.TerminusFacet(args.address)

    print(f"Approving operator: {args.operator}")
    for pool_id in args.pools:
        print(f"Pool ID: {pool_id}")
        terminus.approve_for_pool(pool_id, args.operator, transaction_config)


def handle_unapprove_for_pools(args: argparse.Namespace) -> None:
    network.connect(args.network)
    transaction_config = TerminusFacet.get_transaction_config(args)

    terminus = TerminusFacet.TerminusFacet(args.address)

    print(f"Unapproving operator: {args.operator}")
    for pool_id in args.pools:
        print(f"Pool ID: {pool_id}")
        terminus.unapprove_for_pool(pool_id, args.operator, transaction_config)


parser = argparse.ArgumentParser("Perform operations over multiple Terminus pools")

subparsers = parser.add_subparsers()


pool_controllers_parser = subparsers.add_parser("pool-controllers")
TerminusFacet.add_default_arguments(pool_controllers_parser, False)
add_positional_pool_ids_arg(pool_controllers_parser)
pool_controllers_parser.set_defaults(func=handle_pool_controllers)


balance_parser = subparsers.add_parser("balance-of")
TerminusFacet.add_default_arguments(balance_parser, False)
add_positional_pool_ids_arg(balance_parser)
balance_parser.add_argument("--owner", required=True, help="Address of owner")
balance_parser.set_defaults(func=handle_balance_of)

is_approved_for_pools_parser = subparsers.add_parser("is-approved-for-pools")
TerminusFacet.add_default_arguments(is_approved_for_pools_parser, False)
add_positional_pool_ids_arg(is_approved_for_pools_parser)
is_approved_for_pools_parser.add_argument(
    "--operator", required=True, help="Address of operator"
)
is_approved_for_pools_parser.set_defaults(func=handle_is_approved_for_pools)

approve_for_pools_parser = subparsers.add_parser("approve-for-pools")
TerminusFacet.add_default_arguments(approve_for_pools_parser, True)
add_positional_pool_ids_arg(approve_for_pools_parser)
approve_for_pools_parser.add_argument(
    "--operator", required=True, help="Address of operator"
)
approve_for_pools_parser.set_defaults(func=handle_approve_for_pools)

unapprove_for_pools_parser = subparsers.add_parser("unapprove-for-pools")
TerminusFacet.add_default_arguments(unapprove_for_pools_parser, True)
add_positional_pool_ids_arg(unapprove_for_pools_parser)
unapprove_for_pools_parser.add_argument(
    "--operator", required=True, help="Address of operator"
)
unapprove_for_pools_parser.set_defaults(func=handle_unapprove_for_pools)


args = parser.parse_args()
args.func(args)
