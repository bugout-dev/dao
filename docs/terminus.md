# Terminus: Decentralized authorization

<img src="https://s3.amazonaws.com/static.simiotics.com/dao/terminus-ufo.png" width="250"/>

Terminus is a smart contract which any application can use to track user permissions on Ethereum-based blockchains.

Applications create pools of tokens which represents levels of access to their functionality.
When a blockchain address attempts to use any particular functionality of such an application, the application
checks the token balance of that address to understand whether or not the address is authorized to
access the desired functionality.

Applications can elect to make the tokens in their authorization pools tradable. This allows their users
to trade their access on free, decentralized markets like Open Sea.

Applications can also choose whether or not tokens from their authorization pools get burned when they are
used. This allows them to create authorization pools for limited-use resources (e.g. NFT whitelists)
or for renewable resources (e.g. badges in blockchain games).

The Terminus interface is an extension of the [ERC1155 multi-token interface](https://eips.ethereum.org/EIPS/eip-1155).

## Benefits

### Open markets for authorization

Because Terminus implements the `ERC1155` interface, Terminus authorization tokens can be traded on open
markets.

This is good for users because purchasing access to an application is no longer a sunk cost. It introduces
a sense of liquidity to the notion of access.

For authorizing applications which elect to make their tokens tradable:
1. The market for authorization tokens is the best possible price discovery mechanism for their product
or service.
2. They can forecast usage of their application based on the activity of their authorization tokens on
the market.
3. They operate much closer to capacity because users who are no longer engaged with the application can now
make their authorization available to those with intent to use it.

#### Example: NFT whitelists

Even on popular NFT projects, fewer than 50% of the whitelisted addresses typically exercise their whitelist
privileges. Getting on an NFT whitelist generally requires some effort on the part of a user -- it is
something they have to compete for. If they then do not exercise those privileges -- because they lack
the means or the interest -- it represents a total waste of that effort.

If an NFT project used Terminus to manage its whitelist, these users could sell their whitelist access
on Open Sea, making their effort worthwhile. This would benefit the NFT project, too, by guaranteeing
engaged demand for their tokens.

### Operationally simple

Managing authorizations on a smart contract is not easy, especially if those authorizations heavily
involve state.

The only purpose of Terminus is to manage authorizations and authorization state. This means that, over time,
it will achieve maximal security and minimal gas overhead for this task.

Terminus exposes its functionality through the simple ERC1155 interface, which makes it very easy to integrate with.

Terminus comes with a web interface, which makes it easy for a team to inspect and manage their authorization
pools collaboratively.

### Transparent

Checking whether an address is authorized to perform an action only requires an `ERC1155` `balanceOf`
call against the relevant Terminus authorization pool.

This means that it is transparent to both the application and the user whether or not they have permission
to do something on the application.

Users can inspect the configuration of each pool to understand the authorization semantics - for example,
if their authorization tokens are burned on use or if they persist.

## The Terminus smart contract

Our reference implementation of Terminus is also the one we are using in production. It is implemented
as a facet on an [EIP2535 proxy](https://eips.ethereum.org/EIPS/eip-2535).

The entrypoint to understanding Terminus functionality is the [`TerminusFacet`](../contracts/terminus/TerminusFacet.sol).

## Status and roadmap

Terminus is currently live on the [Polygon Mumbai testnet](../operations/README.md) and is being used by
our earliest adopters.

We are currently building our roadmap. Our immediate priorities can be found in this repository's issues
using the `terminus` tag: https://github.com/bugout-dev/dao/issues?q=is%3Aissue+is%3Aopen+label%3Aterminus
