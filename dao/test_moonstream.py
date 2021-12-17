from brownie import accounts

from . import ERC20Facet, ERC20Initializer
from .core import facet_cut
from .test_core import MoonstreamDAOTestCase


class TestDeployment(MoonstreamDAOTestCase):
    def test_add_and_replace(self):
        initializer = ERC20Initializer.ERC20Initializer(None)
        initializer.deploy({"from": accounts[0]})

        erc20_facet = ERC20Facet.ERC20Facet(None)
        erc20_facet.deploy({"from": accounts[0]})

        diamond_address = self.contracts["Diamond"]
        facet_cut(
            diamond_address,
            "ERC20Facet",
            erc20_facet.address,
            "add",
            {"from": accounts[0]},
            initializer.address,
        )

        diamond_erc20 = ERC20Facet.ERC20Facet(diamond_address)
        name = diamond_erc20.name()
        expected_name = "Moonstream DAO"
        self.assertEqual(name, expected_name)

        symbol = diamond_erc20.symbol()
        expected_symbol = "MNSTR"
        self.assertEqual(symbol, expected_symbol)

        decimals = diamond_erc20.decimals()
        expected_decimals = 18
        self.assertEqual(decimals, expected_decimals)

        with self.assertRaises(Exception):
            diamond_erc20.set_erc20_metadata("LOL", "ROFL", {"from": accounts[1]})

        diamond_erc20.set_erc20_metadata("LOL", "ROFL", {"from": accounts[0]})

        name = diamond_erc20.name()
        expected_name = "LOL"
        self.assertEqual(name, expected_name)

        symbol = diamond_erc20.symbol()
        expected_symbol = "ROFL"
        self.assertEqual(symbol, expected_symbol)

        new_erc20_facet = ERC20Facet.ERC20Facet(None)
        new_erc20_facet.deploy({"from": accounts[0]})
        facet_cut(
            diamond_address,
            "ERC20Facet",
            new_erc20_facet.address,
            "replace",
            {"from": accounts[0]},
            initializer.address,
        )

        name = diamond_erc20.name()
        expected_name = "Moonstream DAO"
        self.assertEqual(name, expected_name)

        symbol = diamond_erc20.symbol()
        expected_symbol = "MNSTR"
        self.assertEqual(symbol, expected_symbol)
