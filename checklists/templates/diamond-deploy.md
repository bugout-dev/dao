# Deploy a diamond proxy

Moonstream DAO uses the EIP2535 Diamond proxy to manage each of its smart contracts.

This checklist describes how to deploy the proxy contract.

## Environment variables

1. `export DAO_NETWORK=<desired brownie network>`
2. `export DAO_OWNER=<path to keystore file for owner account>`
3. `export DAO_OWNER_ADDRESS=$(jq -r .address $DAO_OWNER)`
4. `export GAS_PRICE="<N> gwei"`
5. `export CONFIRMATIONS=<M>`
6. `export OUTPUT_FILE=<path to JSON file in which to store diamond addresses>`

## Deploy diamond proxy

- [ ] Deploy diamond with all core facets

```bash
dao core gogogo \
    --network $DAO_NETWORK \
    --sender $DAO_OWNER \
    --gas-price "$GAS_PRICE" \
    --confirmations $CONFIRMATIONS \
    --owner $DAO_OWNER_ADDRESS \
    --outfile $OUTPUT_FILE
```
