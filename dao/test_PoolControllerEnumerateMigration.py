from typing import List
import unittest

from brownie import accounts
from brownie.exceptions import VirtualMachineError
from sqlalchemy import true

from . import TerminusFacet, PoolControllerEnumeration
from .core import facet_cut
from .test_core import MoonstreamDAOSingleContractTestCase


class TestPoolControllerEnumerationMigration(MoonstreamDAOSingleContractTestCase):
    def test_storage_migration(self):
        initializer = PoolControllerEnumeration.PoolControllerEnumeration(None)
        initializer.deploy({"from": accounts[0]})

        terminus_facet = TerminusFacet.TerminusFacet(None)
        terminus_facet.deploy({"from": accounts[0]})

        diamond_address = self.contracts["Diamond"]
        facet_cut(
            diamond_address,
            "TerminusFacet",
            terminus_facet.address,
            "replace",
            {"from": accounts[0]},
            initializer.address,
        )

        diamond_terminus = TerminusFacet.TerminusFacet(diamond_address)

        controllerPools0 = diamond_terminus.get_controller_pools(accounts[0].address)
        diamond_terminus.create_simple_pool(1,{"from": accounts[0]})
        controllerPools1 = diamond_terminus.get_controller_pools(accounts[0].address)
        self.assertEqual(len(controllerPools0)+1, len(controllerPools1))
        self.assertDictContainsSubset(controllerPools0, controllerPools1)
        for poolId in range(diamond_terminus.total_pools()):
            controller = diamond_terminus.terminus_pool_controller(poolId)
            is_enumerated = False
            if poolId in diamond_terminus.controllerPools1:
                is_enumerated = True
            if controller == accounts[0].address:
                self.assertTrue(is_enumerated)
            else:
                self.assertFalse(is_enumerated)

    def test_pool_enum_after_transfer(self):
        diamond_address = self.contracts["Diamond"]
        diamond_terminus = TerminusFacet.TerminusFacet(diamond_address)
        diamond_terminus.assert_contract_is_instantiated





if __name__ == "__main__":
    unittest.main()
