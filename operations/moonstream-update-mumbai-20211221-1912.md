# Update ERC20Facet on the Moonstream platform token

The Moonstream DAO platform token is deployed as an EIP2535 Diamond proxy contract with an ERC20
facet attached to it.

This checklist describes how to deploy the token.

## Deployed addresses

You will modify this section as you go through the checklist

### `ERC20Facet` address

```
export ERC20FACET_ADDRESS="0x973359bC17de4B2A84Fe3151B5B857f12cf423CB"
```

## Environment variables

- [x] `export DAO_NETWORK=<desired brownie network>`
- [x] `export DAO_OWNER=<path to keystore file for owner account>`
- [x] `export DAO_OWNER_ADDRESS=$(jq -r .address $DAO_OWNER)`
- [x] `export GAS_PRICE="<N> gwei"`
- [x] `export CONFIRMATIONS=<M>`
- [x] `export MOONSTREAM_ADDRESSES=<path to JSON file in which to store diamond addresses>`
- [x] `export MOONSTREAM_DIAMOND="$(jq -r .Diamond $MOONSTREAM_ADDRESSES)"`

## Deploy `ERC20Facet`

- [x] Deploy `ERC20Facet` contract

```bash
dao moonstream deploy \
    --network $DAO_NETWORK \
    --sender $DAO_OWNER \
    --gas-price "$GAS_PRICE" \
    --confirmations $CONFIRMATIONS
```

- [x] Export address of deployed contract as `export ERC20FACET_ADDRESS=<address>`

- [x] Store address of deployed contract under `Deployed addresses / ERC20Facet address` above

- [x] Remove old `ERC20Facet` from diamond.

This may require you to check out a different commit and compile at that commit.

```bash
dao core facet-cut \
    --address $MOONSTREAM_DIAMOND \
    --network $DAO_NETWORK \
    --sender $DAO_OWNER \
    --gas-price "$GAS_PRICE" \
    --confirmations $CONFIRMATIONS \
    --facet-name ERC20Facet \
    --facet-address $ERC20FACET_ADDRESS \
    --action remove
```

- [x] Attach `ERC20Facet` to diamond.

Check out correct commit and do a `brownie compile`.

```bash
dao core facet-cut \
    --address $MOONSTREAM_DIAMOND \
    --network $DAO_NETWORK \
    --sender $DAO_OWNER \
    --gas-price "$GAS_PRICE" \
    --confirmations $CONFIRMATIONS \
    --facet-name ERC20Facet \
    --facet-address $ERC20FACET_ADDRESS \
    --action add
```

- [x] Check the ERC20 name of the diamond contract: `dao moonstream name --network $DAO_NETWORK --address $MOONSTREAM_DIAMOND`

- [x] Name is `Moonstream DAO`

- [x] Check the ERC20 symbol of the diamond contract: `dao moonstream symbol --network $DAO_NETWORK --address $MOONSTREAM_DIAMOND`

- [x] Symbol is `MNSTR`

- [x] Check the controller of the diamond contract: `dao moonstream moonstream-controller --network $DAO_NETWORK --address $MOONSTREAM_DIAMOND`

- [x] Controller is `$DAO_OWNER_ADDRESS`
