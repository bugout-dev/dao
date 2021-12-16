# Moonstream DAO Whitepaper

## Abstract

## Implementation

### ICO

#### Initial Liquidity pool

To ensure appropriate fair initial circulating supply of governance tokens released to a market, a mechanism of automated price discovery is proposed.
In contrast with initial circulating supply being sold by one member of the community, automatied price discovery mechanism is a way for DAO to sell its governance tokens directly.

###### algorithm

_Automated price discovery algorithm_ (APDA) is implemented and deployed in form of smart contract.
At the launch, this contract is supplyed by DAO with share of the community supply of the token.
These tokens are locked for price discovery stage, duration of which is set by DAO.

Over the course of this ICO stage, Members of the community will be able to deposit ETH or MoonstreamDAO tokens.

The ratio of ETH/MoonstreamDAO within the contract will fluctuate, but no swapping can happen and users will be able to withraw the tokens they put in.

At the end of price discovery stage, all of these tokens will be used to create the ETH/MoonstreamDAO liquidity pool, establishing the initial price for the token at the DEX contract.

DAO, and everyone who deposited ETH or MoonstreamDAO will then be able to claim liquidity provider tokens, that track their share of the pool. These LP tokens represent _both_ MoonstreamDAO and ETH assets.
Final result is as if everyone who participated swapped half of their deposited assets for another, collectively, at the same price.

##### Benefits

1. All this brings a decentralized spirit in, the initial liquidity will come from DAO itself and will be owned by DAO, and act with it based on community decisions.

2. Neglecting common price patern of "pump and dump". When token price is initially priced too low, the price correction builds up a momentum, community members fear missing out and they continue to buy the coin until it is dramatically overpiced; This creates a bubble which eventually ends and those who sell at the top make profits of the many more who brought on the rise.
   In APDA model unhealthy price discovery happens in sandboxed enviroment everyone shares the net result to establish initial coin price.

3. Finally, this allows us to fund rise money more efficiently, because we avoid initially underpricing token.


