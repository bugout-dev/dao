# Set up the Terminus contract

This checklist describes how to activate the Terminus contract so that projects can start using it for
decentralized authorization.

## Environment variables

- [ ] `export DAO_NETWORK=<desired brownie network>`
- [ ] `export DAO_OWNER=<path to keystore file for owner account>`
- [ ] `export DAO_OWNER_ADDRESS=$(jq -r .address $DAO_OWNER)`
- [ ] `export GAS_PRICE="<N> gwei"`
- [ ] `export CONFIRMATIONS=<M>`
- [ ] `export MOONSTREAM_DIAMOND=<address of Moonstream token diamond proxy>`
- [ ] `export TERMINUS_DIAMOND=<address of Terminus diamond proxy>`
- [ ] `export TERMINUS_POOL_BASE_PRICE=<base price for creation of Terminus pools>`

## Set up Terminus so that people can create pools

- [ ] Set pool base price:

```bash
dao terminus set-pool-base-price \
    --network $DAO_NETWORK \
    --address $TERMINUS_DIAMOND \
    --sender $DAO_OWNER \
    --gas-price "$GAS_PRICE" \
    --confirmations $CONFIRMATIONS \
    --new-base-price $TERMINUS_POOL_BASE_PRICE
```

- [ ] Check pool base price: `dao terminus pool-base-price --network $DAO_NETWORK --address $TERMINUS_DIAMOND`

- [ ] Pool base price should be same as `$TERMINUS_POOL_BASE_PRICE`

- [ ] Set up payment token:

```bash
dao terminus set-payment-token \
    --network $DAO_NETWORK \
    --address $TERMINUS_DIAMOND \
    --sender $DAO_OWNER \
    --gas-price "$GAS_PRICE" \
    --confirmations $CONFIRMATIONS \
    --new-payment-token $MOONSTREAM_DIAMOND
```

- [ ] Check payment token: `dao terminus payment-token --network $DAO_NETWORK --address $TERMINUS_DIAMOND`

- [ ] Payment token should be same as `$MOONSTREAM_DIAMOND`
