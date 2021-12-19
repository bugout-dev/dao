# Deploy the Moonstream platform token

The Moonstream DAO platform token is deployed as an EIP2535 Diamond proxy contract with an ERC20
facet attached to it.

This checklist describes how to deploy the token.

## Deployed addresses

You will modify this section as you go through the checklist

### Diamond addresses

```json
{
  "DiamondCutFacet": "0x65f8857B204968c492B17344E1139229bD3382e3",
  "Diamond": "0x02620263be8A046Ca4812723596934AA20D7DC3C",
  "DiamondLoupeFacet": "0xeFdFbAA07AF132AD4b319054d91a2F487b009003",
  "OwnershipFacet": "0xA9E3B4BF878d66E213A988B761Ac0774bFc0F1c8",
  "attached": [
    "DiamondLoupeFacet",
    "OwnershipFacet"
  ]
}
```

### `ERC20Initializer` address

```
export ERC20INITIALIZER_ADDRESS=0x6995cA60BE357a72bFAC88a24A05E978637f7Ffb
```

### `ERC20Facet` address

```
export ERC20FACET_ADDRESS=0xC4E53007B5319E73878E4209450A41307Db9de5C
```

## Environment variables

- [x] `export DAO_NETWORK=mumbai`
- [x] `export DAO_OWNER=.secrets/dao-dev.json`
- [x] `export DAO_OWNER_ADDRESS=$(jq -r .address $DAO_OWNER)`
- [x] `export GAS_PRICE="60 gwei"`
- [x] `export CONFIRMATIONS=2`
- [x] `export MOONSTREAM_ADDRESSES=.secrets/moonstream-mumbai-diamond.json`
- [x] `export MOONSTREAM_TOTAL_SUPPLY=10000000000`

## Deploy diamond proxy

- [x] Deploy diamond with all core facets

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

- [x] Export address of deployed contract as `export ERC20INITIALIZER_ADDRESS=0x6995cA60BE357a72bFAC88a24A05E978637f7Ffb`

- [x] Store address of deployed contract under `Deployed addresses / ERC20Initializer address` above


## Deploy `ERC20Facet`

- [x] Deploy `ERC20Facet` contract

```bash
dao moonstream deploy \
    --network $DAO_NETWORK \
    --sender $DAO_OWNER \
    --gas-price "$GAS_PRICE" \
    --confirmations $CONFIRMATIONS
```

- [x] Export address of deployed contract as `export ERC20FACET_ADDRESS=0xC4E53007B5319E73878E4209450A41307Db9de5C`

- [x] Store address of deployed contract under `Deployed addresses / ERC20Facet address` above

- [x] Attach `ERC20Facet` to diamond:

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
