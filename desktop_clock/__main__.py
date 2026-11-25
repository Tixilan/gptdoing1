import argparse

from desktop_clock.app import main, smoke_test


def cli() -> int:
    parser = argparse.ArgumentParser(description="Desktop Clock / 桌面时钟")
    parser.add_argument(
        "--smoke-test",
        action="store_true",
        help="verify the packaged application without opening a window",
    )
    args = parser.parse_args()
    if args.smoke_test:
        smoke_test()
        return 0
    main()
    return 0


if __name__ == "__main__":
    raise SystemExit(cli())

