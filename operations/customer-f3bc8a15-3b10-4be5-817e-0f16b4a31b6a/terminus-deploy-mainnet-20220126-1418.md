# Deploy the Terminus contract

The Terminus contract is deployed as an EIP2535 Diamond proxy contract with a Terminus facet attached to it.

This checklist describes how to deploy the contract.

## Deployed addresses

You will modify this section as you go through the checklist

### Diamond addresses

```
export TERMINUS_DIAMOND="0x99A558BDBdE247C2B2716f0D4cFb0E246DFB697D"
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
- [x] `export MAX_FEE_PER_GAS="1000 gwei"`
- [x] `export MAX_PRIORITY_FEE_PER_GAS="35 gwei"`
- [x] `export CONFIRMATIONS=5`
- [x] `export TERMINUS_ADDRESSES=.secrets/terminus-mainnet-diamond.json`
- [x] `export DIAMOND_CUT_FACET_ADDRESS=$(jq -r .DiamondCutFacet $TERMINUS_ADDRESSES)`
- [x] `export DIAMOND_LOUPE_FACET_ADDRESS=$(jq -r .DiamondLoupeFacet $TERMINUS_ADDRESSES)`
- [x] `export OWNERSHIP_FACET_ADDRESS=$(jq -r .OwnershipFacet $TERMINUS_ADDRESSES)`
- [x] `export TERMINUS_FACET_ADDRESS=0x9718FA06867D2939981151D193cF7ee2B924aec0`
- [x] `export TERMINUS_INITIALIZER_ADDRESS=0x7BcBEE435544bD6F2B2c892040d5B7cD1B00fec7`
- [x] `export WETH=0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619`
- [x] `export TERMINUS_POOL_BASE_PRICE=10000000000000000`

## Deployment

- [x] Deploy diamond

```bash
dao core diamond deploy \
    --network $DAO_NETWORK \
    --sender $DAO_OWNER \
    --max-fee-per-gas "$MAX_FEE_PER_GAS" \
    --max-priority-fee-per-gas "$MAX_PRIORITY_FEE_PER_GAS" \
    --confirmations $CONFIRMATIONS \
    --contract-owner-arg $DAO_OWNER_ADDRESS \
    --diamond-cut-facet-arg $DIAMOND_CUT_FACET_ADDRESS
```

- [x] Store JSON output under `Deployed addresses / Diamond addresses` above.

- [x] Export diamond proxy address: `export TERMINUS_DIAMOND="0x99A558BDBdE247C2B2716f0D4cFb0E246DFB697D"`

- [x] Attach `DiamondLoupeFacet` to diamond:

```bash
dao core facet-cut \
    --address $TERMINUS_DIAMOND \
    --network $DAO_NETWORK \
    --sender $DAO_OWNER \
    --max-fee-per-gas "$MAX_FEE_PER_GAS" \
    --max-priority-fee-per-gas "$MAX_PRIORITY_FEE_PER_GAS" \
    --confirmations $CONFIRMATIONS \
    --facet-name DiamondLoupeFacet \
    --facet-address $DIAMOND_LOUPE_FACET_ADDRESS \
    --action add
```

- [x] Attach `OwnershipFacet` to diamond:

```bash
dao core facet-cut \
    --address $TERMINUS_DIAMOND \
    --network $DAO_NETWORK \
    --sender $DAO_OWNER \
    --max-fee-per-gas "$MAX_FEE_PER_GAS" \
    --max-priority-fee-per-gas "$MAX_PRIORITY_FEE_PER_GAS" \
    --confirmations $CONFIRMATIONS \
    --facet-name OwnershipFacet \
    --facet-address $OWNERSHIP_FACET_ADDRESS \
    --action add
```

- [x] Attach `TerminusFacet` to diamond:

```bash
dao core facet-cut \
    --address $TERMINUS_DIAMOND \
    --network $DAO_NETWORK \
    --sender $DAO_OWNER \
    --max-fee-per-gas "$MAX_FEE_PER_GAS" \
    --max-priority-fee-per-gas "$MAX_PRIORITY_FEE_PER_GAS" \
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

- [x] Set pool base price:

```bash
dao terminus set-pool-base-price \
    --network $DAO_NETWORK \
    --address $TERMINUS_DIAMOND \
    --sender $DAO_OWNER \
    --max-fee-per-gas "$MAX_FEE_PER_GAS" \
    --max-priority-fee-per-gas "$MAX_PRIORITY_FEE_PER_GAS" \
    --confirmations $CONFIRMATIONS \
    --new-base-price $TERMINUS_POOL_BASE_PRICE
```

- [x] Check pool base price: `dao terminus pool-base-price --network $DAO_NETWORK --address $TERMINUS_DIAMOND`

- [x] Pool base price should be same as `$TERMINUS_POOL_BASE_PRICE`

- [x] Set up payment token:

```bash
dao terminus set-payment-token \
    --network $DAO_NETWORK \
    --address $TERMINUS_DIAMOND \
    --sender $DAO_OWNER \
    --max-fee-per-gas "$MAX_FEE_PER_GAS" \
    --max-priority-fee-per-gas "$MAX_PRIORITY_FEE_PER_GAS" \
    --confirmations $CONFIRMATIONS \
    --new-payment-token $WETH
```

- [x] Check payment token: `dao terminus payment-token --network $DAO_NETWORK --address $TERMINUS_DIAMOND`

- [x] Payment token should be same as `$WETH`
