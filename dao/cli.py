import argparse

from . import (
    core,
    ERC20Facet,
    ERC20Initializer,
    TerminusFacet,
    TerminusInitializer,
    MoonstreamTokenFaucet,
    TerminusControllerFacet,
)


def main():
    parser = argparse.ArgumentParser(
        description="dao: The command line interface to Moonstream DAO"
    )
    parser.set_defaults(func=lambda _: parser.print_help())
    dao_subparsers = parser.add_subparsers()

    core_parser = core.generate_cli()
    dao_subparsers.add_parser("core", parents=[core_parser], add_help=False)

    moonstream_parser = ERC20Facet.generate_cli()
    dao_subparsers.add_parser("moonstream", parents=[moonstream_parser], add_help=False)

    moonstream_initializer_parser = ERC20Initializer.generate_cli()
    dao_subparsers.add_parser(
        "moonstream-initializer",
        parents=[moonstream_initializer_parser],
        add_help=False,
    )

    terminus_parser = TerminusFacet.generate_cli()
    dao_subparsers.add_parser("terminus", parents=[terminus_parser], add_help=False)

    terminus_initializer_parser = TerminusInitializer.generate_cli()
    dao_subparsers.add_parser(
        "terminus-initializer",
        parents=[terminus_initializer_parser],
        add_help=False,
    )

    moonstream_token_faucet_parser = MoonstreamTokenFaucet.generate_cli()
    dao_subparsers.add_parser(
        "faucet",
        parents=[moonstream_token_faucet_parser],
        add_help=False,
    )

    terminus_controller_parser = TerminusControllerFacet.generate_cli()
    dao_subparsers.add_parser(
        "terminus-controller", parents=[terminus_controller_parser], add_help=False
    )

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
