# Update the Terminus contract

The Terminus contract is deployed as an EIP2535 Diamond proxy contract with a Terminus facet attached to it.

This checklist describes how to update the `TerminusFacet` on the Terminus diamond contract.

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
- [ ] `export TERMINUS_DIAMOND=<address of Terminus diamond proxy>`

## Detach existing `TerminusFacet`

- [ ] Remove `TerminusFacet` from diamond. (This may require checkout of earlier commit and `brownie compile`.)

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

## Deploy `TerminusInitializer`

- [ ] Check out relevant commit and `brownie compile`.

- [ ] Deploy `TerminusInitializer` contract

```bash
dao moonstream-initializer deploy \
    --network $DAO_NETWORK \
    --sender $DAO_OWNER \
    --gas-price "$GAS_PRICE" \
    --confirmations $CONFIRMATIONS
```

- [ ] Export address of deployed contract as `export TERMINUS_INITIALIZER_ADDRESS=<address>`

- [ ] Store address of deployed contract under `Deployed addresses / TerminusInitializer address` above


## Deploy `TerminusFacet`

- [ ] Check out relevant commit and `brownie compile`.

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
