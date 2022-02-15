# Deploy the Terminus contract

The Terminus contract is deployed as an EIP2535 Diamond proxy contract with a Terminus facet attached to it.

This checklist describes how to deploy the contract.

## Deployed addresses

You will modify this section as you go through the checklist

### Diamond addresses

```json
    "DiamondCutFacet": "0xf0a60Ff27Dc5EA4F1d41bff4799aa35cF78Ddbb6",
    "Diamond": "0x8f4B03662622B9fda5054654742DD805376Bb9C4",
    "DiamondLoupeFacet": "0x5A135598A3E2aEeE611494339D8903a607F79ec2",
    "OwnershipFacet": "0xDd958CC7B61Ca1B0e70917D12d8Efb11B1d80137",

```

### `TerminusInitializer` address

```
export TERMINUS_INITIALIZER_ADDRESS="0xFd2EdFDd88caBD73B448D50514cBd536A2d7F4b6"
```

### `TerminusFacet` address

```
export TERMINUS_FACET_ADDRESS="0xaFc1e94D0670020EF8337bf8bEffBC4bee7873aF"
```

## Environment variables

- [x] `export DAO_NETWORK=<desired brownie network>`
- [x] `export DAO_OWNER=<path to keystore file for owner account>`
- [x] `export DAO_OWNER_ADDRESS=$(jq -r .address $DAO_OWNER)`
- [x] `export GAS_PRICE="<N> gwei"`
- [x] `export CONFIRMATIONS=<M>`
- [x] `export TERMINUS_ADDRESSES=<path to JSON file in which to store diamond addresses>`

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

- [x] Export address of deployed contract as `export TERMINUS_INITIALIZER_ADDRESS=<address>`

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

- [x] Export address of deployed contract as `export TERMINUS_FACET_ADDRESS=<address>`

- [x] Store address of deployed contract under `Deployed addresses / TerminusFacet address` above

- [ ] Attach `TerminusFacet` to diamond:

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

- [ ] Check the Terminus controller: `dao terminus terminus-controller --network $DAO_NETWORK --address $TERMINUS_DIAMOND`

- [ ] Controller should be the same as `$DAO_OWNER_ADDRESS`
