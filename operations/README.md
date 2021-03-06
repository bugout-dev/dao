# Moonstream DAO operations

These documents and checklists represent operations performed against live Moonstream DAO contracts on public
blockchains.

Unless otherwise specified, all operations are executed from the `main` branch of this repository.

## Polygon mainnet

### Current addresses

Terminus: `0x062BEc5e84289Da2CD6147E0e4DA402B33B8f796`

### Operations

- [Deployment of Terminus contract](./terminus-deploy-mainnet-20220121-0704.md) - January 21, 2022
- [Terminus contract setup](./terminus-setup-mainnet-20220121-0704.md) - January 21, 2022

### Parameters

Terminus payment token: Wrapped Ether at `0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619`

Terminus pool base price: `0.01 WETH`


## Polygon Mumbai testnet

### Current addresses

Moonstream platform token (MNSTR): `0x02620263be8A046Ca4812723596934AA20D7DC3C`

Terminus: `0x040Cf7Ee9752936d8d280062a447eB53808EBc08`

Moonstream token faucet: `0x008dB85178d557a5612941131FDF75028422Df33`

### Operations

- [Deployment of Moonstream platform token](./moonstream-deploy-mumbai-20211218-1633.md) - December 18, 2021
- [Update to Moonstream platform token](./moonstream-update-mumbai-20211221-1912.md) - December 21, 2021
- [Deployment of Terminus contract](./terminus-deploy-mumbai-20211222-2028.md) - December 22, 2021
- [Terminus contract setup](./terminus-setup-20211222-2049.md) - December 22, 2021

## Templates

Common operations are available as templates:
- [Deploy Moonstream DAO diamond contracts](./templates/diamond-deploy.md). We use [EIP2535 Diamond proxies](https://eips.ethereum.org/EIPS/eip-2535)
for all our smart contracts. This template describes how to deploy the core diamond proxy contracts that
comprise each component of Moonstream DAO functionality.
- [Deploy the Moonstream platform token](./templates/moonstream-deploy.md)
- [Update functionality on the Moonstream platform token](./templates/moonstream-update.md)
- [Deploy the Terminus smart contract](./templates/terminus-deploy.md)
- [Set up the Terminus smart contract](./templates/terminus-setup.md). This configures payment settings
on a deployed Terminus contract.
