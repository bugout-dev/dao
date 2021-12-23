# Deploy the Terminus contract

The Terminus contract is deployed as an EIP2535 Diamond proxy contract with a Terminus facet attached to it.

This checklist describes how to deploy the contract.

## Deployed addresses

You will modify this section as you go through the checklist

### Diamond addresses

```json
{
  "DiamondCutFacet": "0xda30781C3c8d4c81804E6Bf5c02D5E7898180dd7",
  "Diamond": "0x040Cf7Ee9752936d8d280062a447eB53808EBc08",
  "DiamondLoupeFacet": "0xEC5d886Bc5A7Fc31C76A5aB144c65C75AFa73Aea",
  "OwnershipFacet": "0x2725E9FE8f5C97400d324C529e9ACBAd213E68b9",
  "attached": [
    "DiamondLoupeFacet",
    "OwnershipFacet"
  ]
}
```

### `TerminusInitializer` address

```
export TERMINUS_INITIALIZER_ADDRESS="0xba71CB745C499D4A4f42Fd7aA40044b3b27Da6D4"
```


### `TerminusFacet` address

```
export TERMINUS_FACET_ADDRESS="0x9784e26967779e62450Eb204077EF70B4c7A3612"
```

## Environment variables

- [x] `export DAO_NETWORK=polygon-test`
- [x] `export DAO_OWNER=.secrets/dao-dev.json`
- [x] `export DAO_OWNER_ADDRESS=$(jq -r .address $DAO_OWNER)`
- [x] `export GAS_PRICE="35 gwei"`
- [x] `export CONFIRMATIONS=2`
- [x] `export TERMINUS_ADDRESSES=.secrets/terminus-mumbai-diamond.json`

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

- [x] Export address of deployed contract as `export TERMINUS_INITIALIZER_ADDRESS=0xba71CB745C499D4A4f42Fd7aA40044b3b27Da6D4`

- [x] Store address of deployed contract under `Deployed addresses / TerminusInitializer address` above


## Deploy `TerminusFacet`

- [x] Deploy `TerminusFacet` contract

```bash
dao terminus deploy \
    --network $DAO_NETWORK \
    --sender $DAO_OWNER \
    --gas-price "$GAS_PRICE" \
    --confirmations $CONFIRMATIONS
```

- [x] Export address of deployed contract as `export TERMINUS_FACET_ADDRESS=0x9784e26967779e62450Eb204077EF70B4c7A3612`

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
