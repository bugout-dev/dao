"""
Create a Terminus pool and set its metadata
"""

import argparse

from brownie import network

from dao import TerminusFacet, ERC20Facet

parser = argparse.ArgumentParser("Create a Terminus pool and set its metadata")
TerminusFacet.add_default_arguments(parser, transact=True)
parser.add_argument(
    "--capacity",
    type=int,
    default=2**256 - 1,
    help="Maximum number of tokens in pool (default: 2^256 - 1)",
)
parser.add_argument(
    "--transferable",
    required=True,
    type=TerminusFacet.boolean_argument_type,
    help="Should pool be transferable? ('y' or 'yes' or 1 for yes, 'n' or 'no' or 0 for no)",
)
parser.add_argument(
    "--burnable",
    required=True,
    type=TerminusFacet.boolean_argument_type,
    help="Should pool be burnable? ('y' or 'yes' or 1 for yes, 'n' or 'no' or 0 for no)",
)
parser.add_argument(
    "--uri", default=None, help="Set this if you would like to set a pool metadata URI"
)


args = parser.parse_args()

network.connect(args.network)
transaction_config = TerminusFacet.get_transaction_config(args)
sender = transaction_config["from"]

terminus_contract = TerminusFacet.TerminusFacet(args.address)
payment_token_address = terminus_contract.payment_token()
pool_price = terminus_contract.pool_base_price()

payment_token = ERC20Facet.ERC20Facet(payment_token_address)

sender_balance = payment_token.balance_of(sender.address)
assert (
    sender_balance >= pool_price
), f"Insufficient balance on payment token ({payment_token_address}). Balance: {sender_balance}, required: {pool_price}"

sender_allowance = payment_token.allowance(sender.address, args.address)
if sender_allowance < pool_price:
    print(f"Approve purchase with payment token ({payment_token_address}):")
    payment_token.approve(args.address, pool_price, transaction_config)

print("Creating pool")
receipt = terminus_contract.create_pool_v1(
    args.capacity, args.transferable, args.burnable, transaction_config
)

pool_id = terminus_contract.total_pools(block_number=receipt.block_number)
print(f"Pool created on Terminus contract ({args.address}). Pool ID: {pool_id}")

if args.uri:
    print(
        f"Setting pool URI. Terminus: {args.address}, Pool ID: {pool_id}, URI: {args.uri}"
    )
    terminus_contract.set_uri(pool_id, args.uri, transaction_config)
