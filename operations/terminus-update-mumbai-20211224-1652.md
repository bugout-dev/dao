# Update the Terminus contract

The Terminus contract is deployed as an EIP2535 Diamond proxy contract with a Terminus facet attached to it.

This checklist describes how to update the `TerminusFacet` on the Terminus diamond contract.

## Deployed addresses

You will modify this section as you go through the checklist


### `TerminusFacet` address

```
export TERMINUS_FACET_ADDRESS="0x7Ad8FaD0897f531743817ae0BF43b682f7a0fB67"
```

## Environment variables

- [x] `export DAO_NETWORK=polygon-test`
- [x] `export DAO_OWNER=.secrets/dao-dev.json`
- [x] `export DAO_OWNER_ADDRESS=$(jq -r .address $DAO_OWNER)`
- [x] `export GAS_PRICE="35 gwei"`
- [x] `export CONFIRMATIONS=2`
- [x] `export TERMINUS_DIAMOND=0x040Cf7Ee9752936d8d280062a447eB53808EBc08`

## Detach existing `TerminusFacet`

- [x] Remove `TerminusFacet` from diamond. (This may require checkout of earlier commit and `brownie compile`. Checked out: `v0.0.1`.)

```bash
dao core facet-cut \
    --address $TERMINUS_DIAMOND \
    --network $DAO_NETWORK \
    --sender $DAO_OWNER \
    --gas-price "$GAS_PRICE" \
    --confirmations $CONFIRMATIONS \
    --facet-name TerminusFacet \
    --action remove
```


## Deploy `TerminusFacet`

- [x] Check out relevant commit and `brownie compile`.

- [ ] Deploy `TerminusFacet` contract

```bash
dao terminus deploy \
    --network $DAO_NETWORK \
    --sender $DAO_OWNER \
    --gas-price "$GAS_PRICE" \
    --confirmations $CONFIRMATIONS
```

- [x] Export address of deployed contract as `export TERMINUS_FACET_ADDRESS=0x7Ad8FaD0897f531743817ae0BF43b682f7a0fB67`

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
    --action add
```
