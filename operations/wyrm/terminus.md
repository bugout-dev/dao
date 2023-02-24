# The Great Wyrm Terminus contract

## Deployed addresses

### Diamond addresses

```json
{
  "DiamondCutFacet": "0x59F85f5EF3ab84d0Acbebc7B7c24ea8dD13A51F6",
  "Diamond": "0x49ca1F6801c085ABB165a827baDFD6742a3f8DBc",
  "DiamondLoupeFacet": "0xe65507aF6BaC7d76e6Ee8944967e301e3D6aB632",
  "OwnershipFacet": "0x730B911a9bE224514FC80E3df0E9D0Ad96130c2C",
  "attached": [
    "DiamondLoupeFacet",
    "OwnershipFacet"
  ]
}
```

### `TerminusInitializer` address

```
export TERMINUS_INITIALIZER_ADDRESS="0xaFa971f89874D1CA2825d7fC318291984Cb82863"
```


### `TerminusFacet` address

```
export TERMINUS_FACET_ADDRESS="0x9c10710CA5797DA2878B6FA6E62eC6C1A196416C"
```

## Environment variables

- [x] `export DAO_NETWORK=wyrm`
- [x] `export DAO_OWNER=<path to keystore file for owner account>`
- [x] `export DAO_OWNER_ADDRESS=$(jq -r .address $DAO_OWNER)`
- [x] `export GAS_PRICE=0`
- [x] `export CONFIRMATIONS=1`
- [x] `export TERMINUS_ADDRESSES=<path to JSON file in which to store diamond addresses>`

## Deploy diamond proxy

- [x] Deploy diamond with all core facets

```bash
dao core gogogo \
    --network $DAO_NETWORK \
    --sender $DAO_OWNER \
    --gas-price "$GAS_PRICE" \
    --confirmations $CONFIRMATIONS \
    --owner $DAO_OWNER_ADDRESS \
    --outfile $TERMINUS_ADDRESSES
```

- [x] Store JSON output under `Deployed addresses / Diamond addresses` above.

- [x] Export diamond proxy address: `export TERMINUS_DIAMOND="$(jq -r .Diamond $TERMINUS_ADDRESSES)"`


## Deploy `TerminusInitializer`

- [x] Deploy `TerminusInitializer` contract

```bash
dao terminus-initializer deploy \
    --network $DAO_NETWORK \
    --sender $DAO_OWNER \
    --gas-price "$GAS_PRICE" \
    --confirmations $CONFIRMATIONS
```

- [x] Export address of deployed contract as `export TERMINUS_INITIALIZER_ADDRESS="0xaFa971f89874D1CA2825d7fC318291984Cb82863"`

- [x] Store address of deployed contract under `Deployed addresses / TerminusInitializer address` above


## Deploy `TerminusFacet`

- [x] Deploy `TerminusFacet` contract

```bash
dao terminus deploy \
    --network $DAO_NETWORK \
    --sender $DAO_OWNER \
    --gas-price "$GAS_PRICE" \
    --confirmations $CONFIRMATIONS
```

- [x] Export address of deployed contract as `export TERMINUS_FACET_ADDRESS="0x9c10710CA5797DA2878B6FA6E62eC6C1A196416C"`

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
    --action add \
    --initializer-address $TERMINUS_INITIALIZER_ADDRESS
```

- [x] Check the number of pools on the Terminus contract: `dao terminus total-pools --network $DAO_NETWORK --address $TERMINUS_DIAMOND`

- [x] Number of pools is `0`

- [x] Check the Terminus controller: `dao terminus terminus-controller --network $DAO_NETWORK --address $TERMINUS_DIAMOND`

- [x] Controller should be the same as `$DAO_OWNER_ADDRESS`
