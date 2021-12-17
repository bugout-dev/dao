# Deploy the Moonstream governance token

The Moonstream DAO governance token is deployed as an EIP2535 Diamond proxy contract with an ERC20
facet attached to it.

This checklist describes how to deploy the token.

## Deployed addresses

You will modify this section as you go through the checklist

### Diamond addresses

```json
```

### ERC20Facet address

``

## Environment variables

1. `export DAO_NETWORK=<desired brownie network>`
2. `export DAO_OWNER=<path to keystore file for owner account>`
3. `export DAO_OWNER_ADDRESS=$(jq -r .address $DAO_OWNER)`
4. `export GAS_PRICE="<N> gwei"`
5. `export CONFIRMATIONS=<M>`
6. `export MOONSTREAM_ADDRESSES=<path to JSON file in which to store diamond addresses>`

## Deploy diamond proxy

- [ ] Deploy diamond with all core facets

```bash
dao core gogogo \
    --network $DAO_NETWORK \
    --sender $DAO_OWNER \
    --gas-price "$GAS_PRICE" \
    --confirmations $CONFIRMATIONS \
    --owner $DAO_OWNER_ADDRESS \
    --outfile $MOONSTREAM_ADDRESSES
```

- [ ] Store JSON output under `Deployed addresses / Diamond addresses` above.

## Attach ERC20 functionality

- [ ] Export diamond proxy address: `export MOONSTREAM_DIAMOND="$(jq -r .Diamond $MOONSTREAM_ADDRESSES)"`

- [ ] Deploy `ERC20Facet` contract.

```bash
dao moonstream deploy \
    --network $DAO_NETWORK \
    --sender $DAO_OWNER \
    --gas-price "$GAS_PRICE" \
    --confirmations $CONFIRMATIONS
```

- [ ] Export address of deployed contract as `export ERC20FACET_ADDRESS=<address>`

- [ ] Store address of deployed contract under `Deployed addresses / ERC20Facet address` above

- [ ] Attach `ERC20Facet` to diamond:

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

- [ ] Check the ERC20 name of the diamond contract
