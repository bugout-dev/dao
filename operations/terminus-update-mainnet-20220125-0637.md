# Update the Terminus contract

The Terminus contract is deployed as an EIP2535 Diamond proxy contract with a Terminus facet attached to it.

This checklist describes how to update the `TerminusFacet` on the Terminus diamond contract.

## Deployed addresses

You will modify this section as you go through the checklist


### `TerminusFacet` address

```
export TERMINUS_FACET_ADDRESS="0x9718FA06867D2939981151D193cF7ee2B924aec0"
```

## Environment variables

- [x] `export DAO_NETWORK=matic`
- [x] `export DAO_OWNER=<path to keystore>`
- [x] `export DAO_OWNER_ADDRESS=$(jq -r .address $DAO_OWNER)`
- [x] `export GAS_PRICE="300 gwei"`
- [x] `export CONFIRMATIONS=5`
- [x] `export TERMINUS_DIAMOND=0x062BEc5e84289Da2CD6147E0e4DA402B33B8f796`

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
    --action remove \
    --ignore-methods contractURI setContractURI
```


## Deploy `TerminusFacet`

- [x] Deploy `TerminusFacet` contract

```bash
dao terminus deploy \
    --network $DAO_NETWORK \
    --sender $DAO_OWNER \
    --gas-price "$GAS_PRICE" \
    --confirmations $CONFIRMATIONS
```

- [x] Export address of deployed contract as `export TERMINUS_FACET_ADDRESS=0x9718FA06867D2939981151D193cF7ee2B924aec0`

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
