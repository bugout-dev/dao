# Deploy the Terminus contract

The Terminus contract is deployed as an EIP2535 Diamond proxy contract with a Terminus facet attached to it.

This checklist describes how to deploy the contract.

## Deployed addresses

You will modify this section as you go through the checklist

### Diamond addresses

```json
```

### `TerminusInitializer` address

```
export TERMINUS_INITIALIZER_ADDRESS=""
```


### `TerminusFacet` address

```
export TERMINUS_FACET_ADDRESS=""
```

## Environment variables

- [ ] `export DAO_NETWORK=<desired brownie network>`
- [ ] `export DAO_OWNER=<path to keystore file for owner account>`
- [ ] `export DAO_OWNER_ADDRESS=$(jq -r .address $DAO_OWNER)`
- [ ] `export GAS_PRICE="<N> gwei"`
- [ ] `export CONFIRMATIONS=<M>`
- [ ] `export TERMINUS_ADDRESSES=<path to JSON file in which to store diamond addresses>`

## Deploy diamond proxy

- [ ] Deploy diamond with all core facets

```bash
dao core gogogo \
    --network $DAO_NETWORK \
    --sender $DAO_OWNER \
    --gas-price "$GAS_PRICE" \
    --confirmations $CONFIRMATIONS \
    --owner $DAO_OWNER_ADDRESS \
    --outfile $TERMINUS_ADDRESSES
```

- [ ] Store JSON output under `Deployed addresses / Diamond addresses` above.

- [ ] Export diamond proxy address: `export TERMINUS_DIAMOND="$(jq -r .Diamond $TERMINUS_ADDRESSES)"`


## Deploy `TerminusInitializer`

- [ ] Deploy `TerminusInitializer` contract

```bash
dao terminus-initializer deploy \
    --network $DAO_NETWORK \
    --sender $DAO_OWNER \
    --gas-price "$GAS_PRICE" \
    --confirmations $CONFIRMATIONS
```

- [ ] Export address of deployed contract as `export TERMINUS_INITIALIZER_ADDRESS=<address>`

- [ ] Store address of deployed contract under `Deployed addresses / TerminusInitializer address` above


## Deploy `TerminusFacet`

- [ ] Deploy `TerminusFacet` contract

```bash
dao terminus deploy \
    --network $DAO_NETWORK \
    --sender $DAO_OWNER \
    --gas-price "$GAS_PRICE" \
    --confirmations $CONFIRMATIONS
```

- [ ] Export address of deployed contract as `export TERMINUS_FACET_ADDRESS=<address>`

- [ ] Store address of deployed contract under `Deployed addresses / TerminusFacet address` above

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

- [ ] Check the number of pools on the Terminus contract: `dao terminus total-pools --network $DAO_NETWORK --address $TERMINUS_DIAMOND`

- [ ] Number of pools is `0`

- [ ] Check the Terminus controller: `dao terminus terminus-controller --network $DAO_NETWORK --address $TERMINUS_DIAMOND`

- [ ] Controller should be the same as `$DAO_OWNER_ADDRESS`
