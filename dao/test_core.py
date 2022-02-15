import unittest

from brownie import accounts, network

from .core import facet_cut, gogogo
from .ERC20Facet import ERC20Facet
from .ERC20Initializer import ERC20Initializer
from . import TerminusFacet
from . import TerminusInitializer, PoolControllerEnumeration
from .fixtures import TerminusFacetFixture, TerminusInitializerFixture


class MoonstreamDAOSingleContractTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        try:
            network.connect()
        except:
            pass
        cls.contracts = gogogo(accounts[0], {"from": accounts[0]})


class MoonstreamTokenTestCase(MoonstreamDAOSingleContractTestCase):
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


class TerminusTestCase(MoonstreamTokenTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.terminus_contracts = gogogo(accounts[0], {"from": accounts[0]})

        # Deploy Terminus
        initializer = TerminusInitializer.TerminusInitializer(None)
        initializer.deploy({"from": accounts[0]})

        terminus_facet = TerminusFacet.TerminusFacet(None)
        terminus_facet.deploy({"from": accounts[0]})

        diamond_address = cls.terminus_contracts["Diamond"]
        facet_cut(
            diamond_address,
            "TerminusFacet",
            terminus_facet.address,
            "add",
            {"from": accounts[0]},
            initializer.address,
        )

        cls.terminus_initializer = initializer.address
        cls.terminus_facet = terminus_facet.address


class TerminusFixtureTestCase(MoonstreamTokenTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.terminus_fixture_contracts = gogogo(accounts[0], {"from": accounts[0]})

        # Deploy Terminus
        fixture_initializer = TerminusInitializerFixture.TerminusInitializerFixture(
            None
        )
        fixture_initializer.deploy({"from": accounts[0]})

        terminus_fixture_facet = TerminusFacetFixture.TerminusFacetFixture(None)
        terminus_fixture_facet.deploy({"from": accounts[0]})

        diamond_fixture_address = cls.terminus_fixture_contracts["Diamond"]

        facet_cut(
            diamond_fixture_address,
            "TerminusFacet",
            terminus_fixture_facet.address,
            "add",
            {"from": accounts[0]},
            fixture_initializer.address,
        )

        cls.terminus_fixture_initializer = fixture_initializer.address
        cls.terminus_fixture_facet = terminus_fixture_facet.address


class TestCoreDeployment(MoonstreamDAOSingleContractTestCase):
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
