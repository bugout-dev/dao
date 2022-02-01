# Update the Terminus contract

The Terminus contract is deployed as an EIP2535 Diamond proxy contract with a Terminus facet attached to it.

This checklist describes how to update the `TerminusFacet` on the Terminus diamond contract.

## Deployed addresses

You will modify this section as you go through the checklist

### `TerminusFacet` address

```
export TERMINUS_FACET_ADDRESS="0x6396813307826Fb315e65CA7138A41CFa09a8AB3"
```

## Environment variables

- [x] `export DAO_NETWORK=<desired brownie network>`
- [x] `export DAO_OWNER=<path to keystore file for owner account>`
- [x] `export DAO_OWNER_ADDRESS=$(jq -r .address $DAO_OWNER)`
- [x] `export MAX_FEE_PER_GAS="200 gwei"`
- [x] `export MAX_PRIORITY_FEE_PER_GAS="80 gwei"`
- [x] `export CONFIRMATIONS=1`
- [x] `export TERMINUS_DIAMOND=0x99A558BDBdE247C2B2716f0D4cFb0E246DFB697D`

## Detach existing `TerminusFacet`

- [x] Remove `TerminusFacet` from diamond. (This may require checkout of earlier commit and `brownie compile`.)

```bash
dao core facet-cut \
    --address $TERMINUS_DIAMOND \
    --network $DAO_NETWORK \
    --sender $DAO_OWNER \
    --max-fee-per-gas "$MAX_FEE_PER_GAS" \
    --max-priority-fee-per-gas "$MAX_PRIORITY_FEE_PER_GAS" \
    --confirmations $CONFIRMATIONS \
    --facet-name TerminusFacet \
    --action remove
```


## Deploy `TerminusFacet`

- [x] Check out relevant commit and `brownie compile`.

- [x] Deploy `TerminusFacet` contract

```bash
dao terminus deploy \
    --network $DAO_NETWORK \
    --sender $DAO_OWNER \
    --max-fee-per-gas "$MAX_FEE_PER_GAS" \
    --max-priority-fee-per-gas "$MAX_PRIORITY_FEE_PER_GAS" \
    --confirmations $CONFIRMATIONS
```

- [x] Export address of deployed contract as `export TERMINUS_FACET_ADDRESS=0x6396813307826Fb315e65CA7138A41CFa09a8AB3`

- [x] Store address of deployed contract under `Deployed addresses / TerminusFacet address` above

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
    --action add
```
