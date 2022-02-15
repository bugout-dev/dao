# Deploy the Moonstream platform token

The Moonstream DAO platform token is deployed as an EIP2535 Diamond proxy contract with an ERC20
facet attached to it.

This checklist describes how to deploy the token.

## Deployed addresses

You will modify this section as you go through the checklist

### Diamond addresses

```json
    "DiamondCutFacet": "0x1094297240C4b014b62E29DeD2bcd0352C11Ab78",
    "Diamond": "0x500d73683AF1A2e60887d2885309cD91587015b9",
    "DiamondLoupeFacet": "0x023CE17530ec10202850b038a4c0F2b759bB5EEe",
    "OwnershipFacet": "0x60CAd02d5BeB508835BbfDee13743716f5f04F5b",

```

### `ERC20Initializer` address

```
export ERC20INITIALIZER_ADDRESS=0xAC115be05A69554C45336304A9BCfEC3759Be38a
```

### `ERC20Facet` address

```
export ERC20FACET_ADDRESS="0x65BBC55176eB4d960645A54D5Ad8cFe618A203Cc"
```

## Environment variables

- [x] `export DAO_NETWORK=<desired brownie network>`
- [x] `export DAO_OWNER=<path to keystore file for owner account>`
- [x] `export DAO_OWNER_ADDRESS=$(jq -r .address $DAO_OWNER)`
- [x] `export GAS_PRICE="<N> gwei"`
- [x] `export CONFIRMATIONS=<M>`
- [x] `export MOONSTREAM_ADDRESSES=<path to JSON file in which to store diamond addresses>`
- [x] `export MOONSTREAM_TOTAL_SUPPLY=<number of tokens to mint>`

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

- [x] Store JSON output under `Deployed addresses / Diamond addresses` above.

- [x] Export diamond proxy address: `export MOONSTREAM_DIAMOND="$(jq -r .Diamond $MOONSTREAM_ADDRESSES)"`

## Deploy `ERC20Initializer`

- [x] Deploy `ERC20Initializer` contract

```bash
dao moonstream-initializer deploy \
    --network $DAO_NETWORK \
    --sender $DAO_OWNER \
    --gas-price "$GAS_PRICE" \
    --confirmations $CONFIRMATIONS
```

- [x] Export address of deployed contract as `export ERC20INITIALIZER_ADDRESS=<address>`

- [x] Store address of deployed contract under `Deployed addresses / ERC20Initializer address` above

## Deploy `ERC20Facet`

- [ ] Deploy `ERC20Facet` contract

```bash
dao moonstream deploy \
    --network $DAO_NETWORK \
    --sender $DAO_OWNER \
    --gas-price "$GAS_PRICE" \
    --confirmations $CONFIRMATIONS
```

- [x] Export address of deployed contract as `export ERC20FACET_ADDRESS=<address>`

- [x] Store address of deployed contract under `Deployed addresses / ERC20Facet address` above

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

- [x] Check the ERC20 name of the diamond contract: `dao moonstream name --network $DAO_NETWORK --address $MOONSTREAM_DIAMOND`

- [x] Name is `Moonstream DAO`

- [x] Check the ERC20 symbol of the diamond contract: `dao moonstream symbol --network $DAO_NETWORK --address $MOONSTREAM_DIAMOND`

- [x] Symbol is `MNSTR`

## Mint Moonstream tokens

- [x] Mint `MOONSTREAM_TOTAL_SUPPLY` worth of tokens to self.

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

- [x] Check the total supply of the diamond contract: `dao moonstream total-supply --network $DAO_NETWORK --address $MOONSTREAM_DIAMOND`

- [x] Total supply should be equal to value of `MOONSTREAM_TOTAL_SUPPLY`

- [x] Check balance of DAO owner address: `dao moonstream balance-of --network $DAO_NETWORK --address $MOONSTREAM_DIAMOND --account $DAO_OWNER_ADDRESS`

- [x] Balance should be equal to value of `MOONSTREAM_TOTAL_SUPPLY`
