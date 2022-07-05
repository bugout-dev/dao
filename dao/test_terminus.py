from typing import List
import unittest

from brownie import accounts
from brownie.exceptions import VirtualMachineError

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


class TestController(TerminusTestCase):
    def test_set_controller_fails_when_not_called_by_controller(self):
        terminus_diamond_address = self.terminus_contracts["Diamond"]
        diamond_terminus = TerminusFacet.TerminusFacet(terminus_diamond_address)

        with self.assertRaises(VirtualMachineError):
            diamond_terminus.set_controller(accounts[1].address, {"from": accounts[1]})

    def test_set_controller_fails_when_not_called_by_controller_even_if_they_change_to_existing_controller(
        self,
    ):
        terminus_diamond_address = self.terminus_contracts["Diamond"]
        diamond_terminus = TerminusFacet.TerminusFacet(terminus_diamond_address)

        with self.assertRaises(VirtualMachineError):
            diamond_terminus.set_controller(accounts[0].address, {"from": accounts[1]})

    def test_set_controller(self):
        terminus_diamond_address = self.terminus_contracts["Diamond"]
        diamond_terminus = TerminusFacet.TerminusFacet(terminus_diamond_address)

        self.assertEqual(diamond_terminus.terminus_controller(), accounts[0].address)
        diamond_terminus.set_controller(accounts[3].address, {"from": accounts[0]})
        self.assertEqual(diamond_terminus.terminus_controller(), accounts[3].address)
        diamond_terminus.set_controller(accounts[0].address, {"from": accounts[3]})
        self.assertEqual(diamond_terminus.terminus_controller(), accounts[0].address)


class TestContractURI(TerminusTestCase):
    def test_contract_uri(self):
        terminus_diamond_address = self.terminus_contracts["Diamond"]
        diamond_terminus = TerminusFacet.TerminusFacet(terminus_diamond_address)

        contract_uri = diamond_terminus.contract_uri()
        self.assertEqual(contract_uri, "")

        diamond_terminus.set_contract_uri("https://example.com", {"from": accounts[0]})

        contract_uri = diamond_terminus.contract_uri()
        self.assertEqual(contract_uri, "https://example.com")


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

        diamond_terminus.set_controller(accounts[1].address, {"from": accounts[0]})

        diamond_moonstream.mint(accounts[1], 1000, {"from": accounts[0]})
        initial_payer_balance = diamond_moonstream.balance_of(accounts[1].address)
        initial_terminus_balance = diamond_moonstream.balance_of(
            terminus_diamond_address
        )
        initial_controller_balance = diamond_moonstream.balance_of(accounts[1].address)

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
            accounts[1].address
        )
        self.assertEqual(final_payer_balance, initial_payer_balance - 1000)
        self.assertEqual(intermediate_terminus_balance, initial_terminus_balance + 1000)
        self.assertEqual(
            intermediate_controller_balance, initial_controller_balance - 1000
        )

        with self.assertRaises(Exception):
            diamond_terminus.withdraw_payments(
                accounts[0].address, 1000, {"from": accounts[0]}
            )

        with self.assertRaises(Exception):
            diamond_terminus.withdraw_payments(
                accounts[1].address, 1000, {"from": accounts[0]}
            )

        with self.assertRaises(Exception):
            diamond_terminus.withdraw_payments(
                accounts[0].address, 1000, {"from": accounts[1]}
            )

        diamond_terminus.withdraw_payments(
            accounts[1].address, 1000, {"from": accounts[1]}
        )

        final_terminus_balance = diamond_moonstream.balance_of(terminus_diamond_address)
        final_controller_balance = diamond_moonstream.balance_of(accounts[1].address)
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


class TestPoolOperations(TerminusTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        moonstream_diamond_address = cls.contracts["Diamond"]
        diamond_moonstream = ERC20Facet.ERC20Facet(moonstream_diamond_address)
        terminus_diamond_address = cls.terminus_contracts["Diamond"]
        diamond_terminus = TerminusFacet.TerminusFacet(terminus_diamond_address)
        diamond_terminus.set_payment_token(
            moonstream_diamond_address, {"from": accounts[0]}
        )
        diamond_terminus.set_pool_base_price(1000, {"from": accounts[0]})
        diamond_moonstream.mint(accounts[1], 1000000, {"from": accounts[0]})
        diamond_moonstream.approve(
            terminus_diamond_address, 1000000, {"from": accounts[1]}
        )
        cls.diamond_terminus = diamond_terminus
        cls.diamond_moonstream = diamond_moonstream

        cls.diamond_terminus.set_controller(accounts[1].address, {"from": accounts[0]})

    def setUp(self) -> None:
        self.diamond_terminus.create_simple_pool(10, {"from": accounts[1]})

    def test_set_pool_controller(self):
        pool_id = self.diamond_terminus.total_pools()
        old_controller = accounts[1]
        new_controller = accounts[2]

        current_controller_address = self.diamond_terminus.terminus_pool_controller(
            pool_id
        )
        self.assertEqual(current_controller_address, old_controller.address)

        with self.assertRaises(Exception):
            self.diamond_terminus.set_pool_controller(
                pool_id, new_controller.address, {"from": new_controller}
            )
        current_controller_address = self.diamond_terminus.terminus_pool_controller(
            pool_id
        )
        self.assertEqual(current_controller_address, old_controller.address)

        self.diamond_terminus.set_pool_controller(
            pool_id, new_controller.address, {"from": old_controller}
        )
        current_controller_address = self.diamond_terminus.terminus_pool_controller(
            pool_id
        )
        self.assertEqual(current_controller_address, new_controller.address)

        with self.assertRaises(Exception):
            self.diamond_terminus.set_pool_controller(
                pool_id, old_controller.address, {"from": old_controller}
            )
        current_controller_address = self.diamond_terminus.terminus_pool_controller(
            pool_id
        )
        self.assertEqual(current_controller_address, new_controller.address)

        self.diamond_terminus.set_pool_controller(
            pool_id, old_controller.address, {"from": new_controller}
        )
        current_controller_address = self.diamond_terminus.terminus_pool_controller(
            pool_id
        )
        self.assertEqual(current_controller_address, old_controller.address)

    def test_mint(self):
        pool_id = self.diamond_terminus.total_pools()
        self.diamond_terminus.mint(accounts[2], pool_id, 1, b"", {"from": accounts[1]})

        balance = self.diamond_terminus.balance_of(accounts[2].address, pool_id)
        self.assertEqual(balance, 1)

        supply = self.diamond_terminus.terminus_pool_supply(pool_id)
        self.assertEqual(supply, 1)

    def test_mint_fails_if_it_exceeds_capacity(self):
        pool_id = self.diamond_terminus.total_pools()
        with self.assertRaises(Exception):
            self.diamond_terminus.mint(
                accounts[2], pool_id, 11, b"", {"from": accounts[1]}
            )

        balance = self.diamond_terminus.balance_of(accounts[2].address, pool_id)
        self.assertEqual(balance, 0)

        supply = self.diamond_terminus.terminus_pool_supply(pool_id)
        self.assertEqual(supply, 0)

    def test_mint_batch(self):
        pool_id = self.diamond_terminus.total_pools()
        self.diamond_terminus.mint_batch(
            accounts[2].address,
            pool_i_ds=[pool_id],
            amounts=[1],
            data=b"",
            transaction_config={"from": accounts[1]},
        )

        balance = self.diamond_terminus.balance_of(accounts[2].address, pool_id)
        self.assertEqual(balance, 1)

        supply = self.diamond_terminus.terminus_pool_supply(pool_id)
        self.assertEqual(supply, 1)

    def test_mint_batch_fails_if_it_exceeds_capacity(self):
        pool_id = self.diamond_terminus.total_pools()
        with self.assertRaises(Exception):
            self.diamond_terminus.mint_batch(
                accounts[2].address,
                pool_i_ds=[pool_id],
                amounts=[11],
                data=b"",
                transaction_config={"from": accounts[1]},
            )

        balance = self.diamond_terminus.balance_of(accounts[2].address, pool_id)
        self.assertEqual(balance, 0)

        supply = self.diamond_terminus.terminus_pool_supply(pool_id)
        self.assertEqual(supply, 0)

    def test_pool_mint_batch(self):
        pool_id = self.diamond_terminus.total_pools()
        target_accounts = [account.address for account in accounts[:5]]
        target_amounts = [1 for _ in accounts[:5]]
        num_accounts = len(accounts[:5])
        initial_pool_supply = self.diamond_terminus.terminus_pool_supply(pool_id)
        initial_balances: List[int] = []
        for account in accounts[:5]:
            initial_balances.append(
                self.diamond_terminus.balance_of(account.address, pool_id)
            )
        self.diamond_terminus.pool_mint_batch(
            pool_id, target_accounts, target_amounts, {"from": accounts[1]}
        )
        final_pool_supply = self.diamond_terminus.terminus_pool_supply(pool_id)
        self.assertEqual(final_pool_supply, initial_pool_supply + num_accounts)
        for i, account in enumerate(accounts[:5]):
            final_balance = self.diamond_terminus.balance_of(account.address, pool_id)
            self.assertEqual(final_balance, initial_balances[i] + 1)

    def test_pool_mint_batch_as_contract_controller_not_pool_controller(self):
        pool_id = self.diamond_terminus.total_pools()
        target_accounts = [account.address for account in accounts[:5]]
        target_amounts = [1 for _ in accounts[:5]]
        initial_pool_supply = self.diamond_terminus.terminus_pool_supply(pool_id)
        initial_balances: List[int] = []
        for account in accounts[:5]:
            initial_balances.append(
                self.diamond_terminus.balance_of(account.address, pool_id)
            )
        with self.assertRaises(Exception):
            self.diamond_terminus.pool_mint_batch(
                pool_id, target_accounts, target_amounts, {"from": accounts[0]}
            )
        final_pool_supply = self.diamond_terminus.terminus_pool_supply(pool_id)
        self.assertEqual(final_pool_supply, initial_pool_supply)
        for i, account in enumerate(accounts[:5]):
            final_balance = self.diamond_terminus.balance_of(account.address, pool_id)
            self.assertEqual(final_balance, initial_balances[i])

    def test_pool_mint_batch_as_unauthorized_third_party(self):
        pool_id = self.diamond_terminus.total_pools()
        target_accounts = [account.address for account in accounts[:5]]
        target_amounts = [1 for _ in accounts[:5]]
        initial_pool_supply = self.diamond_terminus.terminus_pool_supply(pool_id)
        initial_balances: List[int] = []
        for account in accounts[:5]:
            initial_balances.append(
                self.diamond_terminus.balance_of(account.address, pool_id)
            )
        with self.assertRaises(Exception):
            self.diamond_terminus.pool_mint_batch(
                pool_id, target_accounts, target_amounts, {"from": accounts[2]}
            )
        final_pool_supply = self.diamond_terminus.terminus_pool_supply(pool_id)
        self.assertEqual(final_pool_supply, initial_pool_supply)
        for i, account in enumerate(accounts[:5]):
            final_balance = self.diamond_terminus.balance_of(account.address, pool_id)
            self.assertEqual(final_balance, initial_balances[i])

    def test_transfer(self):
        pool_id = self.diamond_terminus.total_pools()
        self.diamond_terminus.mint(accounts[2], pool_id, 1, b"", {"from": accounts[1]})

        initial_sender_balance = self.diamond_terminus.balance_of(
            accounts[2].address, pool_id
        )
        initial_receiver_balance = self.diamond_terminus.balance_of(
            accounts[3].address, pool_id
        )

        self.diamond_terminus.safe_transfer_from(
            accounts[2].address,
            accounts[3].address,
            pool_id,
            1,
            b"",
            {"from": accounts[2]},
        )

        final_sender_balance = self.diamond_terminus.balance_of(
            accounts[2].address, pool_id
        )
        final_receiver_balance = self.diamond_terminus.balance_of(
            accounts[3].address, pool_id
        )

        self.assertEqual(final_sender_balance, initial_sender_balance - 1)
        self.assertEqual(final_receiver_balance, initial_receiver_balance + 1)

    def test_transfer_as_pool_controller(self):
        pool_id = self.diamond_terminus.total_pools()
        self.diamond_terminus.mint(accounts[2], pool_id, 1, b"", {"from": accounts[1]})

        initial_sender_balance = self.diamond_terminus.balance_of(
            accounts[2].address, pool_id
        )
        initial_receiver_balance = self.diamond_terminus.balance_of(
            accounts[3].address, pool_id
        )

        self.diamond_terminus.safe_transfer_from(
            accounts[2].address,
            accounts[3].address,
            pool_id,
            1,
            b"",
            {"from": accounts[1]},
        )

        final_sender_balance = self.diamond_terminus.balance_of(
            accounts[2].address, pool_id
        )
        final_receiver_balance = self.diamond_terminus.balance_of(
            accounts[3].address, pool_id
        )

        self.assertEqual(final_sender_balance, initial_sender_balance - 1)
        self.assertEqual(final_receiver_balance, initial_receiver_balance + 1)

    def test_transfer_as_unauthorized_recipient(self):
        pool_id = self.diamond_terminus.total_pools()
        self.diamond_terminus.mint(accounts[2], pool_id, 1, b"", {"from": accounts[1]})

        initial_sender_balance = self.diamond_terminus.balance_of(
            accounts[2].address, pool_id
        )
        initial_receiver_balance = self.diamond_terminus.balance_of(
            accounts[3].address, pool_id
        )

        with self.assertRaises(Exception):
            self.diamond_terminus.safe_transfer_from(
                accounts[2].address,
                accounts[3].address,
                pool_id,
                1,
                b"",
                {"from": accounts[3]},
            )

        final_sender_balance = self.diamond_terminus.balance_of(
            accounts[2].address, pool_id
        )
        final_receiver_balance = self.diamond_terminus.balance_of(
            accounts[3].address, pool_id
        )

        self.assertEqual(final_sender_balance, initial_sender_balance)
        self.assertEqual(final_receiver_balance, initial_receiver_balance)

    def test_transfer_as_authorized_recipient(self):
        pool_id = self.diamond_terminus.total_pools()
        self.diamond_terminus.mint(accounts[2], pool_id, 1, b"", {"from": accounts[1]})

        initial_sender_balance = self.diamond_terminus.balance_of(
            accounts[2].address, pool_id
        )
        initial_receiver_balance = self.diamond_terminus.balance_of(
            accounts[3].address, pool_id
        )

        self.diamond_terminus.approve_for_pool(
            pool_id, accounts[3].address, {"from": accounts[1]}
        )
        self.diamond_terminus.safe_transfer_from(
            accounts[2].address,
            accounts[3].address,
            pool_id,
            1,
            b"",
            {"from": accounts[3]},
        )

        final_sender_balance = self.diamond_terminus.balance_of(
            accounts[2].address, pool_id
        )
        final_receiver_balance = self.diamond_terminus.balance_of(
            accounts[3].address, pool_id
        )

        self.assertEqual(final_sender_balance, initial_sender_balance - 1)
        self.assertEqual(final_receiver_balance, initial_receiver_balance + 1)

    def test_transfer_as_unauthorized_unrelated_party(self):
        pool_id = self.diamond_terminus.total_pools()
        self.diamond_terminus.mint(accounts[2], pool_id, 1, b"", {"from": accounts[1]})

        initial_sender_balance = self.diamond_terminus.balance_of(
            accounts[2].address, pool_id
        )
        initial_receiver_balance = self.diamond_terminus.balance_of(
            accounts[3].address, pool_id
        )

        with self.assertRaises(Exception):
            self.diamond_terminus.safe_transfer_from(
                accounts[2].address,
                accounts[3].address,
                pool_id,
                1,
                b"",
                {"from": accounts[4]},
            )

        final_sender_balance = self.diamond_terminus.balance_of(
            accounts[2].address, pool_id
        )
        final_receiver_balance = self.diamond_terminus.balance_of(
            accounts[3].address, pool_id
        )

        self.assertEqual(final_sender_balance, initial_sender_balance)
        self.assertEqual(final_receiver_balance, initial_receiver_balance)

    def test_transfer_as_authorized_unrelated_party(self):
        pool_id = self.diamond_terminus.total_pools()
        self.diamond_terminus.mint(accounts[2], pool_id, 1, b"", {"from": accounts[1]})

        initial_sender_balance = self.diamond_terminus.balance_of(
            accounts[2].address, pool_id
        )
        initial_receiver_balance = self.diamond_terminus.balance_of(
            accounts[3].address, pool_id
        )

        self.diamond_terminus.approve_for_pool(
            pool_id, accounts[4].address, {"from": accounts[1]}
        )
        self.diamond_terminus.safe_transfer_from(
            accounts[2].address,
            accounts[3].address,
            pool_id,
            1,
            b"",
            {"from": accounts[4]},
        )

        final_sender_balance = self.diamond_terminus.balance_of(
            accounts[2].address, pool_id
        )
        final_receiver_balance = self.diamond_terminus.balance_of(
            accounts[3].address, pool_id
        )

        self.assertEqual(final_sender_balance, initial_sender_balance - 1)
        self.assertEqual(final_receiver_balance, initial_receiver_balance + 1)

    def test_burn_fails_as_token_owner(self):
        pool_id = self.diamond_terminus.total_pools()
        self.diamond_terminus.mint(accounts[2], pool_id, 1, b"", {"from": accounts[1]})

        initial_pool_supply = self.diamond_terminus.terminus_pool_supply(pool_id)
        initial_owner_balance = self.diamond_terminus.balance_of(
            accounts[2].address, pool_id
        )
        with self.assertRaises(Exception):
            self.diamond_terminus.burn(
                accounts[2].address, pool_id, 1, {"from": accounts[2]}
            )

        final_pool_supply = self.diamond_terminus.terminus_pool_supply(pool_id)
        final_owner_balance = self.diamond_terminus.balance_of(
            accounts[2].address, pool_id
        )
        self.assertEqual(final_pool_supply, initial_pool_supply)
        self.assertEqual(final_owner_balance, initial_owner_balance)

    def test_burn_fails_as_pool_controller(self):
        pool_id = self.diamond_terminus.total_pools()
        self.diamond_terminus.mint(accounts[2], pool_id, 1, b"", {"from": accounts[1]})

        initial_pool_supply = self.diamond_terminus.terminus_pool_supply(pool_id)
        initial_owner_balance = self.diamond_terminus.balance_of(
            accounts[2].address, pool_id
        )
        with self.assertRaises(Exception):
            self.diamond_terminus.burn(
                accounts[2].address, pool_id, 1, {"from": accounts[1]}
            )

        final_pool_supply = self.diamond_terminus.terminus_pool_supply(pool_id)
        final_owner_balance = self.diamond_terminus.balance_of(
            accounts[2].address, pool_id
        )
        self.assertEqual(final_pool_supply, initial_pool_supply)
        self.assertEqual(final_owner_balance, initial_owner_balance)

    def test_burn_fails_as_third_party(self):
        pool_id = self.diamond_terminus.total_pools()
        self.diamond_terminus.mint(accounts[2], pool_id, 1, b"", {"from": accounts[1]})

        initial_pool_supply = self.diamond_terminus.terminus_pool_supply(pool_id)
        initial_owner_balance = self.diamond_terminus.balance_of(
            accounts[2].address, pool_id
        )
        with self.assertRaises(Exception):
            self.diamond_terminus.burn(
                accounts[2].address, pool_id, 1, {"from": accounts[3]}
            )

        final_pool_supply = self.diamond_terminus.terminus_pool_supply(pool_id)
        final_owner_balance = self.diamond_terminus.balance_of(
            accounts[2].address, pool_id
        )
        self.assertEqual(final_pool_supply, initial_pool_supply)
        self.assertEqual(final_owner_balance, initial_owner_balance)

    def test_burn_fails_as_authorized_third_party(self):
        pool_id = self.diamond_terminus.total_pools()
        self.diamond_terminus.mint(accounts[2], pool_id, 1, b"", {"from": accounts[1]})

        initial_pool_supply = self.diamond_terminus.terminus_pool_supply(pool_id)
        initial_owner_balance = self.diamond_terminus.balance_of(
            accounts[2].address, pool_id
        )
        self.diamond_terminus.approve_for_pool(
            pool_id, accounts[3].address, {"from": accounts[1]}
        )
        with self.assertRaises(Exception):
            self.diamond_terminus.burn(
                accounts[2].address, pool_id, 1, {"from": accounts[3]}
            )

        final_pool_supply = self.diamond_terminus.terminus_pool_supply(pool_id)
        final_owner_balance = self.diamond_terminus.balance_of(
            accounts[2].address, pool_id
        )
        self.assertEqual(final_pool_supply, initial_pool_supply)
        self.assertEqual(final_owner_balance, initial_owner_balance)


class TestCreatePoolV1(TestPoolOperations):
    def setUp(self):
        self.diamond_terminus.create_pool_v1(10, True, False, {"from": accounts[1]})

    def test_nontransferable_pool(self):
        self.diamond_terminus.create_pool_v1(10, False, False, {"from": accounts[1]})
        pool_id = self.diamond_terminus.total_pools()
        self.diamond_terminus.mint(accounts[2], pool_id, 1, b"", {"from": accounts[1]})

        initial_sender_balance = self.diamond_terminus.balance_of(
            accounts[2].address, pool_id
        )
        initial_receiver_balance = self.diamond_terminus.balance_of(
            accounts[3].address, pool_id
        )

        with self.assertRaises(Exception):
            self.diamond_terminus.safe_transfer_from(
                accounts[2].address,
                accounts[3].address,
                pool_id,
                1,
                b"",
                {"from": accounts[2]},
            )

        final_sender_balance = self.diamond_terminus.balance_of(
            accounts[2].address, pool_id
        )
        final_receiver_balance = self.diamond_terminus.balance_of(
            accounts[3].address, pool_id
        )

        self.assertEqual(final_sender_balance, initial_sender_balance)
        self.assertEqual(final_receiver_balance, initial_receiver_balance)

    def test_pool_state_view_methods(self):
        self.diamond_terminus.create_pool_v1(10, False, False, {"from": accounts[1]})
        nontransferable_nonburnable_pool_id = self.diamond_terminus.total_pools()
        self.assertFalse(
            self.diamond_terminus.pool_is_transferable(
                nontransferable_nonburnable_pool_id
            )
        )
        self.assertFalse(
            self.diamond_terminus.pool_is_burnable(nontransferable_nonburnable_pool_id)
        )

        self.diamond_terminus.create_pool_v1(10, True, False, {"from": accounts[1]})
        transferable_nonburnable_pool_id = self.diamond_terminus.total_pools()
        self.assertTrue(
            self.diamond_terminus.pool_is_transferable(transferable_nonburnable_pool_id)
        )
        self.assertFalse(
            self.diamond_terminus.pool_is_burnable(transferable_nonburnable_pool_id)
        )

        self.diamond_terminus.create_pool_v1(10, True, True, {"from": accounts[1]})
        transferable_burnable_pool_id = self.diamond_terminus.total_pools()
        self.assertTrue(
            self.diamond_terminus.pool_is_transferable(transferable_burnable_pool_id)
        )
        self.assertTrue(
            self.diamond_terminus.pool_is_burnable(transferable_burnable_pool_id)
        )

        self.diamond_terminus.create_pool_v1(10, False, True, {"from": accounts[1]})
        nontransferable_burnable_pool_id = self.diamond_terminus.total_pools()
        self.assertFalse(
            self.diamond_terminus.pool_is_transferable(nontransferable_burnable_pool_id)
        )
        self.assertTrue(
            self.diamond_terminus.pool_is_burnable(nontransferable_burnable_pool_id)
        )

    def test_pool_state_setters(self):
        self.diamond_terminus.create_pool_v1(10, False, False, {"from": accounts[1]})
        pool_id = self.diamond_terminus.total_pools()
        self.assertEqual(
            self.diamond_terminus.terminus_pool_controller(pool_id), accounts[1].address
        )

        self.assertFalse(self.diamond_terminus.pool_is_transferable(pool_id))
        self.assertFalse(self.diamond_terminus.pool_is_burnable(pool_id))

        self.diamond_terminus.set_pool_transferable(
            pool_id, True, {"from": accounts[1]}
        )
        self.assertTrue(self.diamond_terminus.pool_is_transferable(pool_id))
        self.assertFalse(self.diamond_terminus.pool_is_burnable(pool_id))

        self.diamond_terminus.set_pool_burnable(pool_id, True, {"from": accounts[1]})
        self.assertTrue(self.diamond_terminus.pool_is_transferable(pool_id))
        self.assertTrue(self.diamond_terminus.pool_is_burnable(pool_id))

        self.diamond_terminus.set_pool_transferable(
            pool_id, False, {"from": accounts[1]}
        )
        self.assertFalse(self.diamond_terminus.pool_is_transferable(pool_id))
        self.assertTrue(self.diamond_terminus.pool_is_burnable(pool_id))

        self.diamond_terminus.set_pool_burnable(pool_id, False, {"from": accounts[1]})
        self.assertFalse(self.diamond_terminus.pool_is_transferable(pool_id))
        self.assertFalse(self.diamond_terminus.pool_is_burnable(pool_id))

    def test_pool_state_setters_do_not_allow_noncontroller_to_set_parameters(self):
        self.diamond_terminus.create_pool_v1(10, False, False, {"from": accounts[1]})
        pool_id = self.diamond_terminus.total_pools()
        self.assertEqual(
            self.diamond_terminus.terminus_pool_controller(pool_id), accounts[1].address
        )

        self.assertFalse(self.diamond_terminus.pool_is_transferable(pool_id))
        self.assertFalse(self.diamond_terminus.pool_is_burnable(pool_id))

        with self.assertRaises(VirtualMachineError):
            self.diamond_terminus.set_pool_transferable(
                pool_id, True, {"from": accounts[2]}
            )

        with self.assertRaises(VirtualMachineError):
            self.diamond_terminus.set_pool_burnable(
                pool_id, True, {"from": accounts[2]}
            )

        self.assertFalse(self.diamond_terminus.pool_is_transferable(pool_id))
        self.assertFalse(self.diamond_terminus.pool_is_burnable(pool_id))

    def test_burnable_pool_burn_as_token_owner(self):
        self.diamond_terminus.create_pool_v1(10, True, True, {"from": accounts[1]})
        pool_id = self.diamond_terminus.total_pools()
        self.diamond_terminus.mint(accounts[2], pool_id, 1, b"", {"from": accounts[1]})

        initial_pool_supply = self.diamond_terminus.terminus_pool_supply(pool_id)
        initial_owner_balance = self.diamond_terminus.balance_of(
            accounts[2].address, pool_id
        )
        self.diamond_terminus.burn(
            accounts[2].address, pool_id, 1, {"from": accounts[2]}
        )

        final_pool_supply = self.diamond_terminus.terminus_pool_supply(pool_id)
        final_owner_balance = self.diamond_terminus.balance_of(
            accounts[2].address, pool_id
        )
        self.assertEqual(final_pool_supply, initial_pool_supply - 1)
        self.assertEqual(final_owner_balance, initial_owner_balance - 1)

    def test_burnable_pool_burn_as_pool_controller(self):
        self.diamond_terminus.create_pool_v1(10, True, True, {"from": accounts[1]})
        pool_id = self.diamond_terminus.total_pools()
        self.diamond_terminus.mint(accounts[2], pool_id, 1, b"", {"from": accounts[1]})

        initial_pool_supply = self.diamond_terminus.terminus_pool_supply(pool_id)
        initial_owner_balance = self.diamond_terminus.balance_of(
            accounts[2].address, pool_id
        )
        self.diamond_terminus.burn(
            accounts[2].address, pool_id, 1, {"from": accounts[1]}
        )

        final_pool_supply = self.diamond_terminus.terminus_pool_supply(pool_id)
        final_owner_balance = self.diamond_terminus.balance_of(
            accounts[2].address, pool_id
        )
        self.assertEqual(final_pool_supply, initial_pool_supply - 1)
        self.assertEqual(final_owner_balance, initial_owner_balance - 1)

    def test_burnable_pool_burn_as_authorized_third_party(self):
        self.diamond_terminus.create_pool_v1(10, True, True, {"from": accounts[1]})
        pool_id = self.diamond_terminus.total_pools()
        self.diamond_terminus.mint(accounts[2], pool_id, 1, b"", {"from": accounts[1]})

        initial_pool_supply = self.diamond_terminus.terminus_pool_supply(pool_id)
        initial_owner_balance = self.diamond_terminus.balance_of(
            accounts[2].address, pool_id
        )
        self.diamond_terminus.approve_for_pool(
            pool_id, accounts[3].address, {"from": accounts[1]}
        )
        self.diamond_terminus.burn(
            accounts[2].address, pool_id, 1, {"from": accounts[3]}
        )

        final_pool_supply = self.diamond_terminus.terminus_pool_supply(pool_id)
        final_owner_balance = self.diamond_terminus.balance_of(
            accounts[2].address, pool_id
        )
        self.assertEqual(final_pool_supply, initial_pool_supply - 1)
        self.assertEqual(final_owner_balance, initial_owner_balance - 1)

    def test_burnable_pool_burn_as_unauthorized_third_party(self):
        self.diamond_terminus.create_pool_v1(10, True, True, {"from": accounts[1]})
        pool_id = self.diamond_terminus.total_pools()
        self.diamond_terminus.mint(accounts[2], pool_id, 1, b"", {"from": accounts[1]})

        initial_pool_supply = self.diamond_terminus.terminus_pool_supply(pool_id)
        initial_owner_balance = self.diamond_terminus.balance_of(
            accounts[2].address, pool_id
        )
        with self.assertRaises(Exception):
            self.diamond_terminus.burn(
                accounts[2].address, pool_id, 1, {"from": accounts[3]}
            )

        final_pool_supply = self.diamond_terminus.terminus_pool_supply(pool_id)
        final_owner_balance = self.diamond_terminus.balance_of(
            accounts[2].address, pool_id
        )
        self.assertEqual(final_pool_supply, initial_pool_supply)
        self.assertEqual(final_owner_balance, initial_owner_balance)

    def test_nontransferable_pool_safe_transfer_from(self):
        self.diamond_terminus.create_pool_v1(10, False, False, {"from": accounts[1]})
        pool_id = self.diamond_terminus.total_pools()
        self.diamond_terminus.mint(accounts[2], pool_id, 1, b"", {"from": accounts[1]})

        initial_pool_supply = self.diamond_terminus.terminus_pool_supply(pool_id)
        initial_owner_balance = self.diamond_terminus.balance_of(
            accounts[2].address, pool_id
        )
        with self.assertRaises(Exception):
            self.diamond_terminus.safe_transfer_from(
                accounts[2].address,
                accounts[3].address,
                pool_id,
                1,
                b"",
                {"from": accounts[2]},
            )

        final_pool_supply = self.diamond_terminus.terminus_pool_supply(pool_id)
        final_owner_balance = self.diamond_terminus.balance_of(
            accounts[2].address, pool_id
        )
        self.assertEqual(final_pool_supply, initial_pool_supply)
        self.assertEqual(final_owner_balance, initial_owner_balance)

    def test_nontransferable_pool_safe_batch_transfer_from(self):
        self.diamond_terminus.create_pool_v1(10, False, False, {"from": accounts[1]})
        pool_id = self.diamond_terminus.total_pools()
        self.diamond_terminus.mint(accounts[2], pool_id, 1, b"", {"from": accounts[1]})

        initial_pool_supply = self.diamond_terminus.terminus_pool_supply(pool_id)
        initial_owner_balance = self.diamond_terminus.balance_of(
            accounts[2].address, pool_id
        )
        with self.assertRaises(Exception):
            self.diamond_terminus.safe_batch_transfer_from(
                accounts[2].address,
                accounts[3].address,
                [pool_id],
                [1],
                b"",
                {"from": accounts[2]},
            )

        final_pool_supply = self.diamond_terminus.terminus_pool_supply(pool_id)
        final_owner_balance = self.diamond_terminus.balance_of(
            accounts[2].address, pool_id
        )
        self.assertEqual(final_pool_supply, initial_pool_supply)
        self.assertEqual(final_owner_balance, initial_owner_balance)


if __name__ == "__main__":
    unittest.main()
