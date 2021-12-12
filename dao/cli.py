import argparse

from . import diamond


def main():
    parser = argparse.ArgumentParser(
        description="dao: The command line interface to Moonstream DAO"
    )
    parser.set_defaults(func=lambda _: parser.print_help())
    dao_subparsers = parser.add_subparsers()

    diamond_parser = diamond.generate_cli()
    dao_subparsers.add_parser("diamond", parents=[diamond_parser], add_help=False)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
