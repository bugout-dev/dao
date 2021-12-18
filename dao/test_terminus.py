import unittest

from brownie import accounts
import brownie

from . import TerminusFacet, TerminusInitializer
from .core import ZERO_ADDRESS, facet_cut
from .test_core import MoonstreamDAOTestCase, MoonstreamDAOFullTestCase


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


if __name__ == "__main__":
    unittest.main()
