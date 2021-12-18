import unittest

from brownie import accounts
import brownie

from . import ERC20Facet, ERC20Initializer
from .core import ZERO_ADDRESS, facet_cut
from .test_core import MoonstreamDAOTestCase, MoonstreamDAOFullTestCase


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


class TestRemoveFacet(MoonstreamDAOTestCase):
    def test_remove_facet(self):
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

        facet_cut(
            diamond_address,
            "ERC20Facet",
            ZERO_ADDRESS,
            "remove",
            {"from": accounts[0]},
        )

        with self.assertRaises(Exception):
            name = diamond_erc20.name()

        with self.assertRaises(Exception):
            symbol = diamond_erc20.symbol()


class TestERC20(MoonstreamDAOFullTestCase):
    def test_mint_fails_if_not_controller(self):
        diamond_address = self.contracts["Diamond"]
        diamond = ERC20Facet.ERC20Facet(diamond_address)
        with self.assertRaises(Exception):
            diamond.mint(accounts[1].address, 1000, {"from": accounts[1]})

    def test_mint_to_another_address(self):
        diamond_address = self.contracts["Diamond"]
        diamond = ERC20Facet.ERC20Facet(diamond_address)
        initial_balance = diamond.balance_of(accounts[1].address)
        diamond.mint(accounts[1].address, 1000, {"from": accounts[0]})
        final_balance = diamond.balance_of(accounts[1].address)
        self.assertEqual(final_balance, initial_balance + 1000)

    def test_transfer(self):
        diamond_address = self.contracts["Diamond"]
        diamond = ERC20Facet.ERC20Facet(diamond_address)

        diamond.mint(accounts[1].address, 1000, {"from": accounts[0]})

        initial_sender_balance = diamond.balance_of(accounts[1].address)
        initial_receiver_balance = diamond.balance_of(accounts[2].address)

        diamond.transfer(accounts[2].address, 500, {"from": accounts[1]})

        final_sender_balance = diamond.balance_of(accounts[1].address)
        final_receiver_balance = diamond.balance_of(accounts[2].address)

        self.assertEqual(final_sender_balance, initial_sender_balance - 500)
        self.assertEqual(final_receiver_balance, initial_receiver_balance + 500)

    def test_transfer_insufficient_balance(self):
        diamond_address = self.contracts["Diamond"]
        diamond = ERC20Facet.ERC20Facet(diamond_address)

        initial_sender_balance = diamond.balance_of(accounts[1].address)
        initial_receiver_balance = diamond.balance_of(accounts[2].address)

        with self.assertRaises(Exception):
            diamond.transfer(
                accounts[2].address, initial_sender_balance + 1, {"from": accounts[1]}
            )

        final_sender_balance = diamond.balance_of(accounts[1].address)
        final_receiver_balance = diamond.balance_of(accounts[2].address)

        self.assertEqual(final_sender_balance, initial_sender_balance)
        self.assertEqual(final_receiver_balance, initial_receiver_balance)

    def test_transfer_from_with_approval(self):
        diamond_address = self.contracts["Diamond"]
        diamond = ERC20Facet.ERC20Facet(diamond_address)

        diamond.mint(accounts[1].address, 1000, {"from": accounts[0]})

        initial_sender_balance = diamond.balance_of(accounts[1].address)
        initial_receiver_balance = diamond.balance_of(accounts[2].address)

        diamond.approve(accounts[2].address, 500, {"from": accounts[1]})
        diamond.transfer_from(
            accounts[1].address, accounts[2].address, 500, {"from": accounts[2]}
        )

        final_sender_balance = diamond.balance_of(accounts[1].address)
        final_receiver_balance = diamond.balance_of(accounts[2].address)

        self.assertEqual(final_sender_balance, initial_sender_balance - 500)
        self.assertEqual(final_receiver_balance, initial_receiver_balance + 500)

    def test_transfer_with_approval_insufficient_balance(self):
        diamond_address = self.contracts["Diamond"]
        diamond = ERC20Facet.ERC20Facet(diamond_address)

        initial_sender_balance = diamond.balance_of(accounts[1].address)
        initial_receiver_balance = diamond.balance_of(accounts[2].address)

        diamond.approve(
            accounts[2].address, initial_sender_balance + 1, {"from": accounts[1]}
        )

        with self.assertRaises(Exception):
            diamond.transfer_from(
                accounts[1].address,
                accounts[2].address,
                initial_sender_balance + 1,
                {"from": accounts[2]},
            )

        final_sender_balance = diamond.balance_of(accounts[1].address)
        final_receiver_balance = diamond.balance_of(accounts[2].address)

        self.assertEqual(final_sender_balance, initial_sender_balance)
        self.assertEqual(final_receiver_balance, initial_receiver_balance)

    def test_transfer_from_with_approval_insufficient_allowance_sufficient_balance(
        self,
    ):
        diamond_address = self.contracts["Diamond"]
        diamond = ERC20Facet.ERC20Facet(diamond_address)

        diamond.mint(accounts[1].address, 1000, {"from": accounts[0]})
        diamond.approve(accounts[2].address, 500, {"from": accounts[1]})

        initial_sender_balance = diamond.balance_of(accounts[1].address)
        initial_receiver_balance = diamond.balance_of(accounts[2].address)

        with self.assertRaises(Exception):
            diamond.transfer_from(
                accounts[1].address,
                accounts[2].address,
                501,
                {"from": accounts[2]},
            )

        final_sender_balance = diamond.balance_of(accounts[1].address)
        final_receiver_balance = diamond.balance_of(accounts[2].address)

        self.assertEqual(final_sender_balance, initial_sender_balance)
        self.assertEqual(final_receiver_balance, initial_receiver_balance)

    def test_not_burnable(self):
        diamond_address = self.contracts["Diamond"]
        diamond = ERC20Facet.ERC20Facet(diamond_address)

        diamond.mint(accounts[1].address, 1000, {"from": accounts[0]})

        with self.assertRaises(Exception):
            diamond.transfer(brownie.ZERO_ADDRESS, 500, {"from": accounts[1]})

    def test_approve_and_allowance(self):
        diamond_address = self.contracts["Diamond"]
        diamond = ERC20Facet.ERC20Facet(diamond_address)

        diamond.approve(accounts[2].address, 500, {"from": accounts[1]})
        allowance = diamond.allowance(accounts[1].address, accounts[2].address)
        self.assertEqual(allowance, 500)

    def test_increase_allowance(self):
        diamond_address = self.contracts["Diamond"]
        diamond = ERC20Facet.ERC20Facet(diamond_address)

        initial_allowance = diamond.allowance(accounts[1].address, accounts[2].address)

        diamond.increase_allowance(accounts[2].address, 500, {"from": accounts[1]})
        final_allowance = diamond.allowance(accounts[1].address, accounts[2].address)
        self.assertEqual(final_allowance, initial_allowance + 500)

    def test_decrease_allowance(self):
        diamond_address = self.contracts["Diamond"]
        diamond = ERC20Facet.ERC20Facet(diamond_address)

        initial_allowance = diamond.allowance(accounts[1].address, accounts[2].address)

        diamond.decrease_allowance(accounts[2].address, 500, {"from": accounts[1]})
        final_allowance = diamond.allowance(accounts[1].address, accounts[2].address)
        self.assertEqual(final_allowance, initial_allowance - 500)

    def test_mint_total_supply(self):
        diamond_address = self.contracts["Diamond"]
        diamond = ERC20Facet.ERC20Facet(diamond_address)

        initial_total_supply = diamond.total_supply()
        diamond.mint(accounts[1].address, 1000, {"from": accounts[0]})

        final_total_supply = diamond.total_supply()
        self.assertEqual(final_total_supply, initial_total_supply + 1000)


if __name__ == "__main__":
    unittest.main()
