# Set up the Terminus contract

This checklist describes how to activate the Terminus contract so that projects can start using it for
decentralized authorization.

## Environment variables

- [x] `export DAO_NETWORK=polygon-test`
- [x] `export DAO_OWNER=.secrets/dao-dev.json`
- [x] `export DAO_OWNER_ADDRESS=$(jq -r .address $DAO_OWNER)`
- [x] `export GAS_PRICE="35 gwei"`
- [x] `export CONFIRMATIONS=2`
- [x] `export MOONSTREAM_DIAMOND=$(jq -r .Diamond .secrets/moonstream-mumbai-diamond.json)`
- [x] `export TERMINUS_DIAMOND=$(jq -r .Diamond .secrets/terminus-mumbai-diamond.json)`
- [ ] `export TERMINUS_POOL_BASE_PRICE=1000000000000000000`

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
    --new-payment-token $MOONSTREAM_DIAMOND
```

- [x] Check payment token: `dao terminus payment-token --network $DAO_NETWORK --address $TERMINUS_DIAMOND`

- [x] Payment token should be same as `$MOONSTREAM_DIAMOND`
