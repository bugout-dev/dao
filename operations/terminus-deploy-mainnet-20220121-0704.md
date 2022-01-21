# Deploy the Terminus contract

The Terminus contract is deployed as an EIP2535 Diamond proxy contract with a Terminus facet attached to it.

This checklist describes how to deploy the contract.

## Deployed addresses

You will modify this section as you go through the checklist

### Diamond addresses

```json
{
  "DiamondCutFacet": "0x539d0E4A68F720b35c1670B6421673a852de52DB",
  "Diamond": "0x062BEc5e84289Da2CD6147E0e4DA402B33B8f796",
  "DiamondLoupeFacet": "0x024e974B4524f245fE3da60CbD70EC62875f8194",
  "OwnershipFacet": "0x35f2d4877C7a468eA76f2D6666d3D8a487D73A9B",
  "attached": [
    "DiamondLoupeFacet",
    "OwnershipFacet"
  ]
}
```

### `TerminusInitializer` address

```
export TERMINUS_INITIALIZER_ADDRESS="0x7BcBEE435544bD6F2B2c892040d5B7cD1B00fec7"
```


### `TerminusFacet` address

```
export TERMINUS_FACET_ADDRESS="0x63Cf75b3ffE339Ec30524F204a5FfB97813bF9fB"
```

## Environment variables

- [x] `export DAO_NETWORK=matic`
- [x] `export DAO_OWNER=<path to keystore file for owner account>`
- [x] `export DAO_OWNER_ADDRESS=$(jq -r .address $DAO_OWNER)`
- [x] `export GAS_PRICE="300 gwei"`
- [x] `export CONFIRMATIONS=5`
- [x] `export TERMINUS_ADDRESSES=.secrets/terminus-mainnet-diamond.json`

## Deploy diamond proxy

- [x] Deploy diamond with all core facets

```bash
dao core gogogo \
    --network $DAO_NETWORK \
    --sender $DAO_OWNER \
    --gas-price "$GAS_PRICE" \
    --confirmations $CONFIRMATIONS \
    --owner $DAO_OWNER_ADDRESS \
    --outfile $TERMINUS_ADDRESSES
```

- [x] Store JSON output under `Deployed addresses / Diamond addresses` above.

- [x] Export diamond proxy address: `export TERMINUS_DIAMOND="$(jq -r .Diamond $TERMINUS_ADDRESSES)"`


## Deploy `TerminusInitializer`

- [x] Deploy `TerminusInitializer` contract

```bash
dao terminus-initializer deploy \
    --network $DAO_NETWORK \
    --sender $DAO_OWNER \
    --gas-price "$GAS_PRICE" \
    --confirmations $CONFIRMATIONS
```

- [x] Export address of deployed contract as `export TERMINUS_INITIALIZER_ADDRESS=0x7BcBEE435544bD6F2B2c892040d5B7cD1B00fec7`

- [x] Store address of deployed contract under `Deployed addresses / TerminusInitializer address` above

### Notes

Accidentally deployed `ERC20Initializer` to this address: `0x838a510A2A93E1878149760Ed1540A8e7B77D596`.

Fixed the typo in the `terminus-deploy` template.


## Deploy `TerminusFacet`

- [x] Deploy `TerminusFacet` contract

```bash
dao terminus deploy \
    --network $DAO_NETWORK \
    --sender $DAO_OWNER \
    --gas-price "$GAS_PRICE" \
    --confirmations $CONFIRMATIONS
```

- [x] Export address of deployed contract as `export TERMINUS_FACET_ADDRESS=0x63Cf75b3ffE339Ec30524F204a5FfB97813bF9fB`

- [x] Store address of deployed contract under `Deployed addresses / TerminusFacet address` above

- [x] Attach `TerminusFacet` to diamond:

```bash
dao core facet-cut \
    --address $TERMINUS_DIAMOND \
    --network $DAO_NETWORK \
    --sender $DAO_OWNER \
    --gas-price "$GAS_PRICE" \
    --confirmations $CONFIRMATIONS \
    --facet-name TerminusFacet \
    --facet-address $TERMINUS_FACET_ADDRESS \
    --action add \
    --initializer-address $TERMINUS_INITIALIZER_ADDRESS
```

- [x] Check the number of pools on the Terminus contract: `dao terminus total-pools --network $DAO_NETWORK --address $TERMINUS_DIAMOND`

- [x] Number of pools is `0`

- [x] Check the Terminus controller: `dao terminus terminus-controller --network $DAO_NETWORK --address $TERMINUS_DIAMOND`

- [x] Controller should be the same as `$DAO_OWNER_ADDRESS`
