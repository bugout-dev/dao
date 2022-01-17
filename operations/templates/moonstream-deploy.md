# Deploy the Moonstream platform token

The Moonstream DAO platform token is deployed as an EIP2535 Diamond proxy contract with an ERC20
facet attached to it.

This checklist describes how to deploy the token.

## Deployed addresses

You will modify this section as you go through the checklist

### Diamond addresses

```json
```

### `ERC20Initializer` address

```
export ERC20INITIALIZER_ADDRESS=""
```

### `ERC20Facet` address

```
export ERC20FACET_ADDRESS=""
```

## Environment variables

- [ ] `export DAO_NETWORK=<desired brownie network>`
- [ ] `export DAO_OWNER=<path to keystore file for owner account>`
- [ ] `export DAO_OWNER_ADDRESS=$(jq -r .address $DAO_OWNER)`
- [ ] `export GAS_PRICE="<N> gwei"`
- [ ] `export CONFIRMATIONS=<M>`
- [ ] `export MOONSTREAM_ADDRESSES=<path to JSON file in which to store diamond addresses>`
- [ ] `export MOONSTREAM_TOTAL_SUPPLY=<number of tokens to mint>`

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

- [ ] Export diamond proxy address: `export MOONSTREAM_DIAMOND="$(jq -r .Diamond $MOONSTREAM_ADDRESSES)"`

## Deploy `ERC20Initializer`

- [ ] Deploy `ERC20Initializer` contract

```bash
dao moonstream-initializer deploy \
    --network $DAO_NETWORK \
    --sender $DAO_OWNER \
    --gas-price "$GAS_PRICE" \
    --confirmations $CONFIRMATIONS
```

- [ ] Export address of deployed contract as `export ERC20INITIALIZER_ADDRESS=<address>`

- [ ] Store address of deployed contract under `Deployed addresses / ERC20Initializer address` above


## Deploy `ERC20Facet`

- [ ] Deploy `ERC20Facet` contract

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
    --action add \
    --initializer-address $ERC20INITIALIZER_ADDRESS
```

- [ ] Check the ERC20 name of the diamond contract: `dao moonstream name --network $DAO_NETWORK --address $MOONSTREAM_DIAMOND`

- [ ] Name is `Moonstream DAO`

- [ ] Check the ERC20 symbol of the diamond contract: `dao moonstream symbol --network $DAO_NETWORK --address $MOONSTREAM_DIAMOND`

- [ ] Symbol is `MNSTR`

## Mint Moonstream tokens

- [ ] Mint `MOONSTREAM_TOTAL_SUPPLY` worth of tokens to self.

```bash
dao moonstream mint \
    --network $DAO_NETWORK \
    --address $MOONSTREAM_DIAMOND \
    --sender $DAO_OWNER \
    --gas-price "$GAS_PRICE" \
    --confirmations $CONFIRMATIONS \
    --account $DAO_OWNER_ADDRESS \
    --amount $MOONSTREAM_TOTAL_SUPPLY
```

- [ ] Check the total supply of the diamond contract: `dao moonstream total-supply --network $DAO_NETWORK --address $MOONSTREAM_DIAMOND`

- [ ] Total supply should be equal to value of `MOONSTREAM_TOTAL_SUPPLY`

- [ ] Check balance of DAO owner address: `dao moonstream balance-of --network $DAO_NETWORK --address $MOONSTREAM_DIAMOND --account $DAO_OWNER_ADDRESS`

- [ ] Balance should be equal to value of `MOONSTREAM_TOTAL_SUPPLY`
