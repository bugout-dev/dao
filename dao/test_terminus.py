import unittest

from brownie import accounts

from . import TerminusFacet, TerminusInitializer
from .core import facet_cut
from .test_core import MoonstreamDAOTestCase, TerminusTestCase


class TestDeployment(MoonstreamDAOTestCase):
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
    def test_create_pool(self):
        diamond_address = self.contracts["Diamond"]
        diamond_terminus = TerminusFacet.TerminusFacet(diamond_address)

        initial_total_pools = diamond_terminus.total_pools()
        diamond_terminus.create_pool({"from": accounts[1]})
        final_total_pools = diamond_terminus.total_pools()
        self.assertEqual(final_total_pools, initial_total_pools + 1)

        pool_controller = diamond_terminus.terminus_pool_controller(final_total_pools)
        self.assertEqual(pool_controller, accounts[1].address)


if __name__ == "__main__":
    unittest.main()
