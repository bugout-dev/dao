import unittest

from brownie import accounts, network

from dao.core import gogogo


class MoonstreamDAOTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        try:
            network.connect()
        except:
            pass
        cls.contracts = gogogo(accounts[0], {"from": accounts[0]})


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
