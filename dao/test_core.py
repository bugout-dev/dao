import unittest

from brownie import accounts, network

from .core import facet_cut, gogogo
from .ERC20Facet import ERC20Facet
from .ERC20Initializer import ERC20Initializer


class MoonstreamDAOTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        try:
            network.connect()
        except:
            pass
        cls.contracts = gogogo(accounts[0], {"from": accounts[0]})


class MoonstreamDAOFullTestCase(MoonstreamDAOTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        # Deploy ERC20
        initializer = ERC20Initializer(None)
        initializer.deploy({"from": accounts[0]})

        erc20_facet = ERC20Facet(None)
        erc20_facet.deploy({"from": accounts[0]})

        diamond_address = cls.contracts["Diamond"]
        facet_cut(
            diamond_address,
            "ERC20Facet",
            erc20_facet.address,
            "add",
            {"from": accounts[0]},
            initializer.address,
        )

        cls.erc20_initializer = initializer.address
        cls.erc20_facet = erc20_facet.address


class TestCoreDeployment(MoonstreamDAOTestCase):
    def test_gogogo(self):
        self.assertIn("DiamondCutFacet", self.contracts)
        self.assertIn("Diamond", self.contracts)
        self.assertIn("DiamondLoupeFacet", self.contracts)
        self.assertIn("OwnershipFacet", self.contracts)
        self.assertIn("attached", self.contracts)

        self.assertListEqual(
            self.contracts["attached"],
            ["DiamondLoupeFacet", "OwnershipFacet"],
        )


if __name__ == "__main__":
    unittest.main()
