# dao
Moonstream DAO

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

For example, if you modify the `TerminusFacet` contract, you would then run this command:

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
