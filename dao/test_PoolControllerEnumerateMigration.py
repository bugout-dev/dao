from typing import List
import unittest

from brownie import accounts
from brownie.exceptions import VirtualMachineError
from sqlalchemy import true

from . import TerminusFacet, PoolControllerEnumeration, TerminusFacetFixture, TerminusInitializerFixture
from .core import facet_cut
from .test_core import MoonstreamDAOSingleContractTestCase


class TestPoolControllerEnumerationMigration(MoonstreamDAOSingleContractTestCase):
        @classmethod
        def setUpClass(cls) -> None:
            super().setUpClass()

    def test_migration_from_old_state(self):

        # old state
        fixture_initializer = TerminusInitializerFixture.TerminusInitializerFixture(None)
        fixture_initializer.deploy({"from": accounts[0]})

        fixture_terminus_facet = TerminusFacetFixture.TerminusFacetFixture(None)
        fixture_terminus_facet.deploy({"from": accounts[0]})

        # deploy, intialize, setup and test new diamond contract
        

        # facet_cut fixtures onto newly created diamond

        # test that facets are fixtures

        # run standard facet tests

        # replace facet with PoolControllerEnumeration update

        initializer = PoolControllerEnumeration.PoolControllerEnumeration(None)
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

        # test that pool enumeration migrated successfully
        diamond_terminus = TerminusFacet.TerminusFacet(diamond_address)
        for poolId in range(diamond_terminus.total_pools()):
                controller = diamond_terminus.terminus_pool_controller(poolId)







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


    def test_pool_enum_after_transfer(self):
        diamond_address = self.contracts["Diamond"]
        diamond_terminus = TerminusFacet.TerminusFacet(diamond_address)
        diamond_terminus.assert_contract_is_instantiated





if __name__ == "__main__":
    unittest.main()
