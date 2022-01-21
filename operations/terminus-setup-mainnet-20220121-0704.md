# Set up the Terminus contract

This checklist describes how to activate the Terminus contract so that projects can start using it for
decentralized authorization.

## Environment variables

- [x] `export DAO_NETWORK=matic`
- [x] `export DAO_OWNER=<path to keystore file for owner account>`
- [x] `export DAO_OWNER_ADDRESS=$(jq -r .address $DAO_OWNER)`
- [x] `export GAS_PRICE="300 gwei"`
- [x] `export CONFIRMATIONS=5`
- [x] `export WETH=0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619`
- [x] `export TERMINUS_DIAMOND=0x062BEc5e84289Da2CD6147E0e4DA402B33B8f796`
- [x] `export TERMINUS_POOL_BASE_PRICE=10000000000000000`

## Set up Terminus so that people can create pools

- [x] Set pool base price:

```bash
dao terminus set-pool-base-price \
    --network $DAO_NETWORK \
    --address $TERMINUS_DIAMOND \
    --sender $DAO_OWNER \
    --gas-price "$GAS_PRICE" \
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
    --gas-price "$GAS_PRICE" \
    --confirmations $CONFIRMATIONS \
    --new-payment-token $WETH
```

- [x] Check payment token: `dao terminus payment-token --network $DAO_NETWORK --address $TERMINUS_DIAMOND`

- [x] Payment token should be same as `$WETH`
