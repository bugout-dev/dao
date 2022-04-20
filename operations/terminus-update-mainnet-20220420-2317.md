# Update the Terminus contract

The Terminus contract is deployed as an EIP2535 Diamond proxy contract with a Terminus facet attached to it.

This checklist describes how to update the `TerminusFacet` on the Terminus diamond contract.

## Purpose of update

Make `safeBatchTransferFrom` respect non-transferable Terminus pools. (And add `setController`.)

## Deployed addresses

You will modify this section as you go through the checklist

### `TerminusFacet` address

```
export TERMINUS_FACET_ADDRESS="0xaA91032E567fD3CF2e7102f65B1AaF21530583a0"
```

## Environment variables

- [x] `export DAO_NETWORK=polygon-main`
- [x] `export DAO_OWNER=<redacted>`
- [x] `export DAO_OWNER_ADDRESS=$(jq -r .address $DAO_OWNER)`
- [x] `export GAS_PRICE="80 gwei"`
- [x] `export CONFIRMATIONS=5`
- [x] `export TERMINUS_DIAMOND=0x062BEc5e84289Da2CD6147E0e4DA402B33B8f796`
- [x] `export POLYGONSCAN_TOKEN=<redacted>`

## Deploy `TerminusFacet`

- [x] Check out relevant commit and `brownie compile`.

- [x] Deploy `TerminusFacet` contract

```bash
dao terminus deploy \
    --network $DAO_NETWORK \
    --sender $DAO_OWNER \
    --gas-price "$GAS_PRICE" \
    --confirmations $CONFIRMATIONS
```


- [x] Export address of deployed contract as `export TERMINUS_FACET_ADDRESS=0xaA91032E567fD3CF2e7102f65B1AaF21530583a0`

- [x] Store address of deployed contract under `Deployed addresses / TerminusFacet address` above

- [x] Verify `TerminusFacet` contract

```
dao terminus verify-contract --network $DAO_NETWORK --address $TERMINUS_FACET_ADDRESS
```

- [x] Build [Inspector Facet](https://github.com/bugout-dev/inpsector-facet) report for Diamond contract:

```
- - -
Facet at address: 0x539d0E4A68F720b35c1670B6421673a852de52DB
Possible contracts: IDiamondCut, DiamondCutFacet
IDiamondCut:
	Missing methods:
	Mounted selectors:
		Selector: 0x1f931c1c, Function: diamondCut
DiamondCutFacet:
	Missing methods:
	Mounted selectors:
		Selector: 0x1f931c1c, Function: diamondCut
- - -
Facet at address: 0x024e974B4524f245fE3da60CbD70EC62875f8194
Possible contracts: DiamondLoupeFacet
DiamondLoupeFacet:
	Missing methods:
	Mounted selectors:
		Selector: 0xcdffacc6, Function: facetAddress
		Selector: 0x52ef6b2c, Function: facetAddresses
		Selector: 0xadfca15e, Function: facetFunctionSelectors
		Selector: 0x7a0ed627, Function: facets
		Selector: 0x01ffc9a7, Function: supportsInterface
- - -
Facet at address: 0x35f2d4877C7a468eA76f2D6666d3D8a487D73A9B
Possible contracts: OwnershipFacet, IERC173
OwnershipFacet:
	Missing methods:
	Mounted selectors:
		Selector: 0x8da5cb5b, Function: owner
		Selector: 0xf2fde38b, Function: transferOwnership
IERC173:
	Missing methods:
	Mounted selectors:
		Selector: 0x8da5cb5b, Function: owner
		Selector: 0xf2fde38b, Function: transferOwnership
- - -
Facet at address: 0x6396813307826Fb315e65CA7138A41CFa09a8AB3
Possible contracts: TerminusFacet
TerminusFacet:
	Missing methods:
		Missing selector: 0x01ffc9a7, Function: supportsInterface
	Mounted selectors:
		Selector: 0x85bc82e2, Function: approveForPool
		Selector: 0x00fdd58e, Function: balanceOf
		Selector: 0x4e1273f4, Function: balanceOfBatch
		Selector: 0xf5298aca, Function: burn
		Selector: 0xe8a3d485, Function: contractURI
		Selector: 0x3bad2d82, Function: createPoolV1
		Selector: 0xb507ef52, Function: createSimplePool
		Selector: 0xe985e9c5, Function: isApprovedForAll
		Selector: 0x027b3fc2, Function: isApprovedForPool
		Selector: 0x731133e9, Function: mint
		Selector: 0x1f7fdffa, Function: mintBatch
		Selector: 0x3013ce29, Function: paymentToken
		Selector: 0x8925d013, Function: poolBasePrice
		Selector: 0x21adca96, Function: poolMintBatch
		Selector: 0x2eb2c2d6, Function: safeBatchTransferFrom
		Selector: 0xf242432a, Function: safeTransferFrom
		Selector: 0xa22cb465, Function: setApprovalForAll
		Selector: 0x938e3d7b, Function: setContractURI
		Selector: 0x92eefe9b, Function: setController
		Selector: 0x6a326ab1, Function: setPaymentToken
		Selector: 0x78cf2e84, Function: setPoolBasePrice
		Selector: 0xdc55d0b2, Function: setPoolController
		Selector: 0x862440e2, Function: setURI
		Selector: 0x366e59e3, Function: terminusController
		Selector: 0x5dc8bdf8, Function: terminusPoolCapacity
		Selector: 0xd0c402e5, Function: terminusPoolController
		Selector: 0xa44cfc82, Function: terminusPoolSupply
		Selector: 0xab3c7e52, Function: totalPools
		Selector: 0x0e89341c, Function: uri
		Selector: 0x0e7afec5, Function: withdrawPayments
```

- [x] Replace existing `TerminusFacet` methods on diamond:

```bash
dao core facet-cut \
    --address $TERMINUS_DIAMOND \
    --network $DAO_NETWORK \
    --sender $DAO_OWNER \
    --gas-price "$GAS_PRICE" \
    --confirmations $CONFIRMATIONS \
    --facet-name TerminusFacet \
    --facet-address $TERMINUS_FACET_ADDRESS \
    --action replace
```

- [x] Build [Inspector Facet](https://github.com/bugout-dev/inpsector-facet) report for Diamond contract:

```
- - -
Facet at address: 0x539d0E4A68F720b35c1670B6421673a852de52DB
Possible contracts: IDiamondCut, DiamondCutFacet
IDiamondCut:
	Missing methods:
	Mounted selectors:
		Selector: 0x1f931c1c, Function: diamondCut
DiamondCutFacet:
	Missing methods:
	Mounted selectors:
		Selector: 0x1f931c1c, Function: diamondCut
- - -
Facet at address: 0x024e974B4524f245fE3da60CbD70EC62875f8194
Possible contracts: DiamondLoupeFacet
DiamondLoupeFacet:
	Missing methods:
	Mounted selectors:
		Selector: 0xcdffacc6, Function: facetAddress
		Selector: 0x52ef6b2c, Function: facetAddresses
		Selector: 0xadfca15e, Function: facetFunctionSelectors
		Selector: 0x7a0ed627, Function: facets
		Selector: 0x01ffc9a7, Function: supportsInterface
- - -
Facet at address: 0x35f2d4877C7a468eA76f2D6666d3D8a487D73A9B
Possible contracts: OwnershipFacet, IERC173
OwnershipFacet:
	Missing methods:
	Mounted selectors:
		Selector: 0x8da5cb5b, Function: owner
		Selector: 0xf2fde38b, Function: transferOwnership
IERC173:
	Missing methods:
	Mounted selectors:
		Selector: 0x8da5cb5b, Function: owner
		Selector: 0xf2fde38b, Function: transferOwnership
- - -
Facet at address: 0xaA91032E567fD3CF2e7102f65B1AaF21530583a0
Possible contracts: TerminusFacet
TerminusFacet:
	Missing methods:
		Missing selector: 0x01ffc9a7, Function: supportsInterface
	Mounted selectors:
		Selector: 0x85bc82e2, Function: approveForPool
		Selector: 0x00fdd58e, Function: balanceOf
		Selector: 0x4e1273f4, Function: balanceOfBatch
		Selector: 0xf5298aca, Function: burn
		Selector: 0xe8a3d485, Function: contractURI
		Selector: 0x3bad2d82, Function: createPoolV1
		Selector: 0xb507ef52, Function: createSimplePool
		Selector: 0xe985e9c5, Function: isApprovedForAll
		Selector: 0x027b3fc2, Function: isApprovedForPool
		Selector: 0x731133e9, Function: mint
		Selector: 0x1f7fdffa, Function: mintBatch
		Selector: 0x3013ce29, Function: paymentToken
		Selector: 0x8925d013, Function: poolBasePrice
		Selector: 0x21adca96, Function: poolMintBatch
		Selector: 0x2eb2c2d6, Function: safeBatchTransferFrom
		Selector: 0xf242432a, Function: safeTransferFrom
		Selector: 0xa22cb465, Function: setApprovalForAll
		Selector: 0x938e3d7b, Function: setContractURI
		Selector: 0x92eefe9b, Function: setController
		Selector: 0x6a326ab1, Function: setPaymentToken
		Selector: 0x78cf2e84, Function: setPoolBasePrice
		Selector: 0xdc55d0b2, Function: setPoolController
		Selector: 0x862440e2, Function: setURI
		Selector: 0x366e59e3, Function: terminusController
		Selector: 0x5dc8bdf8, Function: terminusPoolCapacity
		Selector: 0xd0c402e5, Function: terminusPoolController
		Selector: 0xa44cfc82, Function: terminusPoolSupply
		Selector: 0xab3c7e52, Function: totalPools
		Selector: 0x0e89341c, Function: uri
		Selector: 0x0e7afec5, Function: withdrawPayments
```
