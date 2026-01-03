"""Command-line helpers for bs4dash-py."""

from __future__ import annotations

from pathlib import Path

from . import list_vendored_bootswatch, serve_vendored_bootswatch


def list_vendored_main() -> None:
    themes = list_vendored_bootswatch()
    if not themes:
        print("No vendored Bootswatch themes found.")
        return
    print("Vendored Bootswatch themes:")
    for t in themes:
        print(f"- {t}")


def serve_vendored_main(dest: str) -> None:
    """Copy vendored themes into the provided destination directory."""
    out = Path(dest)
    copied = serve_vendored_bootswatch(out)
    if not copied:
        print("No vendored themes copied.")
        return
    print(f"Copied {len(copied)} vendored theme files to {out}")


def main() -> None:  # simple dispatcher
    import argparse

    p = argparse.ArgumentParser(prog="bs4dash-cli")
    sub = p.add_subparsers(dest="cmd")
    sub.add_parser("list", help="List vendored Bootswatch themes")
    serve = sub.add_parser("serve", help="Copy vendored themes to a static directory")
    serve.add_argument("dest", help="Destination directory to copy themes into")

    args = p.parse_args()
    if args.cmd == "list":
        list_vendored_main()
    elif args.cmd == "serve":
        serve_vendored_main(args.dest)
    else:
        p.print_help()
