# dao
Moonstream DAO

## Decentralizing Moonstream

[Moonstream](https://moonstream.to) helps you manage all aspects of your decentralized applications,
from whitelisting to authorization to monitoring to product analytics.

Moonstream infrastructure is currently hosted and managed by the team at Bugout.dev (https://bugout.dev).
We run our own blockchain nodes (currently Ethereum and Polygon), and perform all Moonstream operations
through these nodes.

The coming years will bring an explosion of decentralized applications with a presence on multiple
blockchains. We aim to bring the value of Moonstream to *every* major blockchain, and to do so in a
truly decentralized manner. No other approach will scale to tens and eventually hundreds of supported
blockchains.

Moonstream DAO represents this decentralization. The DAO will reward participants who contribute:
1. Blockchain node time
2. Crawler time
3. Crawler code
4. Storage for the Moonstream databases
5. Publicity for Moonstream
6. Documentation
7. Moonstream token liquidity

Rewards will be distributed as a share of revenue, represented in Moonstream platform tokens.

As strong believers in decentralization, all our code is already open source and freely licensed (Apache 2.0
and MIT): https://github.com/bugout-dev. The Moonstream DAO represents the next level of openness and
transparency for Moonstream -- that of our infrastructure and operations.

## Deployments

You can find the addresses for all Moonstream DAO contracts on our [`operations`](./operations/README.md) page.

## Development environment

### Preparing your development environment

Moonstream DAO is built with Solidity, Python, and shell scripts.

We use [`brownie`](https://github.com/eth-brownie/brownie) to build our smart contracts, deploy them,
and perform operations on them.

We use [`moonworm`](https://github.com/bugout-dev/moonworm) to generate Python interfaces to our smart
contracts from their ABIs.

To set up an environment in which you can develop on Moonstream DAO, first create a Python3 environment.

Using the built in `venv` module:

```bash
python3 -m venv .dao
```

Then make sure that this new environment is active. If you used `venv` as above:

```bash
source .dao/bin/activate
```

Finally, install the dependencies and developer dependencies for `dao`:

```bash
pip install -e ".[dev]"
```

### Tests

To run unit tests, run: `./test.sh`

Before you do this, you must make sure that a Python environment is available in your shell and that
you have installed the development dependencies in this environment.

### Development workflow

Every time you add, remove, or modify an `external` or `public` method from a Solidity smart contract in this repository,
make sure to regenerate its Python interface.

You can do this by activating your Python development environment and running the following command from
the repository root:

```bash
moonworm generate-brownie -p . -o dao -n "<name of Solidity contract you modified>"
```

For example, if you modified the `TerminusFacet` contract, you would then run this command:

```bash
moonworm generate-brownie -p . -o dao -n TerminusFacet
```

### VSCode setup

If you are using the Solidity extension in VSCode, merge the following snippet into your settings.json:

```json
{
    "solidity.remappings": [
        "@openzeppelin-contracts/=<path to your home directory>/.brownie/packages/OpenZeppelin/openzeppelin-contracts@4.3.2"
    ]
}
```
