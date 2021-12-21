import unittest

from brownie import accounts

from . import ERC20Facet, TerminusFacet, TerminusInitializer
from .core import facet_cut
from .test_core import MoonstreamDAOSingleContractTestCase, TerminusTestCase


class TestDeployment(MoonstreamDAOSingleContractTestCase):
    def test_add_and_replace(self):
        initializer = TerminusInitializer.TerminusInitializer(None)
        initializer.deploy({"from": accounts[0]})

        terminus_facet = TerminusFacet.TerminusFacet(None)
        terminus_facet.deploy({"from": accounts[0]})

        diamond_address = self.contracts["Diamond"]
        facet_cut(
            diamond_address,
            "TerminusFacet",
            terminus_facet.address,
            "add",
            {"from": accounts[0]},
            initializer.address,
        )

        diamond_terminus = TerminusFacet.TerminusFacet(diamond_address)

        controller = diamond_terminus.terminus_controller()
        self.assertEqual(controller, accounts[0].address)


class TestPoolCreation(TerminusTestCase):
    def test_create_simple_pool(self):
        moonstream_diamond_address = self.contracts["Diamond"]
        diamond_moonstream = ERC20Facet.ERC20Facet(moonstream_diamond_address)

        terminus_diamond_address = self.terminus_contracts["Diamond"]
        diamond_terminus = TerminusFacet.TerminusFacet(terminus_diamond_address)

        diamond_terminus.set_payment_token(
            moonstream_diamond_address, {"from": accounts[0]}
        )
        payment_token = diamond_terminus.payment_token()
        self.assertEqual(payment_token, moonstream_diamond_address)

        diamond_terminus.set_pool_base_price(1000, {"from": accounts[0]})
        pool_base_price = diamond_terminus.pool_base_price()
        self.assertEqual(pool_base_price, 1000)

        diamond_moonstream.mint(accounts[1], 1000, {"from": accounts[0]})
        initial_payer_balance = diamond_moonstream.balance_of(accounts[1].address)
        initial_terminus_balance = diamond_moonstream.balance_of(
            terminus_diamond_address
        )
        initial_controller_balance = diamond_moonstream.balance_of(accounts[0].address)

        diamond_moonstream.approve(
            terminus_diamond_address, 1000, {"from": accounts[1]}
        )

        initial_total_pools = diamond_terminus.total_pools()

        diamond_terminus.create_simple_pool(10, {"from": accounts[1]})

        final_total_pools = diamond_terminus.total_pools()
        self.assertEqual(final_total_pools, initial_total_pools + 1)

        final_payer_balance = diamond_moonstream.balance_of(accounts[1].address)
        intermediate_terminus_balance = diamond_moonstream.balance_of(
            terminus_diamond_address
        )
        intermediate_controller_balance = diamond_moonstream.balance_of(
            accounts[0].address
        )
        self.assertEqual(final_payer_balance, initial_payer_balance - 1000)
        self.assertEqual(intermediate_terminus_balance, initial_terminus_balance + 1000)
        self.assertEqual(intermediate_controller_balance, initial_controller_balance)

        with self.assertRaises(Exception):
            diamond_terminus.withdraw_payments(
                accounts[1].address, 1000, {"from": accounts[1]}
            )

        with self.assertRaises(Exception):
            diamond_terminus.withdraw_payments(
                accounts[0].address, 1000, {"from": accounts[1]}
            )

        with self.assertRaises(Exception):
            diamond_terminus.withdraw_payments(
                accounts[1].address, 1000, {"from": accounts[0]}
            )

        diamond_terminus.withdraw_payments(
            accounts[0].address, 1000, {"from": accounts[0]}
        )

        final_terminus_balance = diamond_moonstream.balance_of(terminus_diamond_address)
        final_controller_balance = diamond_moonstream.balance_of(accounts[0].address)
        self.assertEqual(final_terminus_balance, intermediate_terminus_balance - 1000)
        self.assertEqual(
            final_controller_balance, intermediate_controller_balance + 1000
        )

        with self.assertRaises(Exception):
            diamond_terminus.withdraw_payments(
                accounts[0].address,
                final_terminus_balance + 1000,
                {"from": accounts[0]},
            )

        pool_controller = diamond_terminus.terminus_pool_controller(final_total_pools)
        self.assertEqual(pool_controller, accounts[1].address)

        pool_capacity = diamond_terminus.terminus_pool_capacity(final_total_pools)
        self.assertEqual(pool_capacity, 10)


if __name__ == "__main__":
    unittest.main()
