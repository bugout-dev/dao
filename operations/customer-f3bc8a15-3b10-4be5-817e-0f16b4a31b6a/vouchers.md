# Voucher contract

## Deployed addresses

### Diamond addresses

```json
{
  "DiamondCutFacet": "0x12e5f5dCb0F6c3771aF05a1f57c6a899665efdf1",
  "Diamond": "0x677441c2e95c8Cf3176dF05F45a515c2570C62a4",
  "DiamondLoupeFacet": "0x9EbBE32339eCA1201d14cF2487F2256966372170",
  "OwnershipFacet": "0x852420E735Da8d87728596585E9A67e1424B1FDE",
  "attached": ["DiamondLoupeFacet", "OwnershipFacet"]
}
```

### `TerminusInitializer` address

```
export TERMINUS_INITIALIZER_ADDRESS="0x3d5ffae90F4F5573fC6A348B12059B2dFc5D4147"
```

### `TerminusFacet` address

```
export TERMINUS_FACET_ADDRESS="0x22F4284E1E2a1de9892a5D7c1982C7C2B403DDE9"
```

## Environment variables

- [x] `export DAO_NETWORK=polygon-main`
- [x] `export DAO_OWNER=<path to keystore file for owner account>`
- [x] `export DAO_OWNER_ADDRESS=$(jq -r .address $DAO_OWNER)`
- [x] `export MAX_FEE_PER_GAS="1000 gwei"`
- [x] `export MAX_PRIORITY_FEE_PER_GAS="100 gwei"`
- [x] `export CONFIRMATIONS=4`
- [x] `export TERMINUS_ADDRESSES=operations/customer-f3bc8a15-3b10-4be5-817e-0f16b4a31b6a/voucher.json`

## Deploy diamond proxy

- [x] Deploy diamond with all core facets

```bash
dao core gogogo \
    --network $DAO_NETWORK \
    --sender $DAO_OWNER \
    --max-fee-per-gas "$MAX_FEE_PER_GAS" \
    --max-priority-fee-per-gas "$MAX_PRIORITY_FEE_PER_GAS" \
    --confirmations $CONFIRMATIONS \
    --owner $DAO_OWNER_ADDRESS \
    --outfile $TERMINUS_ADDRESSES
```

- [x] Store JSON output under `Deployed addresses / Diamond addresses` above.

- [x] Export diamond proxy address: `export TERMINUS_DIAMOND="$(jq -r .Diamond $TERMINUS_ADDRESSES)"`

## Deploy `TerminusInitializer`

- [ ] Deploy `TerminusInitializer` contract

```bash
dao terminus-initializer deploy \
    --network $DAO_NETWORK \
    --sender $DAO_OWNER \
    --max-fee-per-gas "$MAX_FEE_PER_GAS" \
    --max-priority-fee-per-gas "$MAX_PRIORITY_FEE_PER_GAS" \
    --confirmations $CONFIRMATIONS
```

- [x] Export address of deployed contract as `export TERMINUS_INITIALIZER_ADDRESS="0x3d5ffae90F4F5573fC6A348B12059B2dFc5D4147"`

- [x] Store address of deployed contract under `Deployed addresses / TerminusInitializer address` above

## Deploy `TerminusFacet`

- [x] Deploy `TerminusFacet` contract

```bash
dao terminus deploy \
    --network $DAO_NETWORK \
    --sender $DAO_OWNER \
    --max-fee-per-gas "$MAX_FEE_PER_GAS" \
    --max-priority-fee-per-gas "$MAX_PRIORITY_FEE_PER_GAS" \
    --confirmations $CONFIRMATIONS
```

- [x] Export address of deployed contract as `export TERMINUS_FACET_ADDRESS="0x22F4284E1E2a1de9892a5D7c1982C7C2B403DDE9"`

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
    --action add \
    --initializer-address $TERMINUS_INITIALIZER_ADDRESS
```

- [x] Check the number of pools on the Terminus contract: `dao terminus total-pools --network $DAO_NETWORK --address $TERMINUS_DIAMOND`

- [x] Number of pools is `0`

- [x] Check the Terminus controller: `dao terminus terminus-controller --network $DAO_NETWORK --address $TERMINUS_DIAMOND`

- [x] Controller should be the same as `$DAO_OWNER_ADDRESS`
