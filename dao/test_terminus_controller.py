from typing import List
import unittest

from brownie import accounts, network
from brownie.exceptions import VirtualMachineError

from . import ERC20Facet, TerminusFacet, TerminusInitializer, TerminusControllerFacet
from .core import facet_cut, gogogo


class TestTerminusController(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        try:
            network.connect()
        except:
            pass
        terminus_diamond_address = gogogo(accounts[0], {"from": accounts[0]})["Diamond"]

        initializer = TerminusInitializer.TerminusInitializer(None)
        initializer.deploy({"from": accounts[0]})

        terminus_facet = TerminusFacet.TerminusFacet(None)
        terminus_facet.deploy({"from": accounts[0]})

        facet_cut(
            terminus_diamond_address,
            "TerminusFacet",
            terminus_facet.address,
            "add",
            {"from": accounts[0]},
            initializer.address,
        )
        cls.terminus = TerminusFacet.TerminusFacet(terminus_diamond_address)

        terminus_controller_diamond_address = gogogo(
            accounts[0], {"from": accounts[0]}
        )["Diamond"]

        terminus_controller_facet = TerminusControllerFacet.TerminusControllerFacet(
            None
        )
        terminus_controller_facet.deploy({"from": accounts[0]})

        facet_cut(
            terminus_controller_diamond_address,
            "TerminusControllerFacet",
            terminus_controller_facet.address,
            "add",
            {"from": accounts[0]},
        )
        cls.terminus_controller = TerminusControllerFacet.TerminusControllerFacet(
            terminus_controller_diamond_address
        )

        erc20_facet = ERC20Facet.ERC20Facet(None)
        erc20_facet.deploy({"from": accounts[0]})

        cls.terminus.set_payment_token(erc20_facet.address, {"from": accounts[0]})
        cls.terminus.create_pool_v1(
            10**18,
            True,
            True,
            {
                "from": accounts[0],
            },
        )

        cls.main_pool_id = 1

        cls.terminus.mint(
            accounts[0],
            cls.main_pool_id,
            1,
            "",
            {"from": accounts[0]},
        )

        cls.terminus_controller.init_terminus_controller(
            cls.terminus.address,
            cls.terminus.address,
            cls.main_pool_id,
            {"from": accounts[0]},
        )

        cls.terminus.set_pool_controller(
            cls.main_pool_id, cls.terminus_controller.address, {"from": accounts[0]}
        )

        cls.terminus.set_controller(
            cls.terminus_controller.address,
            {"from": accounts[0]},
        )

    def test_proxy_mint(self):
        balance_before = self.terminus.balance_of(accounts[1], self.main_pool_id)
        self.terminus_controller.mint(
            accounts[1],
            self.main_pool_id,
            1,
            "",
            {"from": accounts[0]},
        )
        balance_after = self.terminus.balance_of(accounts[1], self.main_pool_id)
        self.assertEqual(balance_after, balance_before + 1)

    def test_create_new_pool_fails_without_permissions(self):
        main_admin_pool_balance = self.terminus.balance_of(
            accounts[1], self.main_pool_id
        )
        if main_admin_pool_balance > 0:
            self.terminus_controller.burn(
                accounts[1],
                self.main_pool_id,
                main_admin_pool_balance,
                {"from": accounts[0]},
            )

        with self.assertRaises(Exception):
            self.terminus_controller.create_pool_v1(
                10**18, True, True, {"from": accounts[1]}
            )

    def test_create_new_pool(self):
        self.terminus_controller.mint(
            accounts[1], self.main_pool_id, 1, "", {"from": accounts[0]}
        )

        self.terminus_controller.create_pool_v1(
            10**18,
            True,
            True,
            {
                "from": accounts[1],
            },
        )
        self.terminus_controller.create_pool_v1(
            10**18,
            True,
            True,
            {
                "from": accounts[1],
            },
        )

        new_pool_id = self.terminus_controller.total_pools()
        controller_pool_id = new_pool_id - 1

        self.terminus_controller.set_pool_control_permissions(
            new_pool_id,
            self.terminus.address,
            controller_pool_id,
            {"from": accounts[1]},
        )

        with self.assertRaises(Exception):
            self.terminus_controller.mint(
                accounts[4].address, new_pool_id, 1, "", {"from": accounts[3]}
            )

        self.terminus_controller.mint(
            accounts[3].address, controller_pool_id, 1, "", {"from": accounts[1]}
        )

        self.terminus_controller.mint(
            accounts[4].address, new_pool_id, 1, "", {"from": accounts[3]}
        )
        self.assertEqual(self.terminus.balance_of(accounts[4], new_pool_id), 1)


if __name__ == "__main__":
    unittest.main()
