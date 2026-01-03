#!/usr/bin/env python3
"""Small utility to list vendored Bootswatch themes in this package."""
from bs4dash_py import list_vendored_bootswatch


def main():
    themes = list_vendored_bootswatch()
    if not themes:
        print("No vendored Bootswatch themes found.")
    else:
        print("Vendored Bootswatch themes:")
        for t in themes:
            print(f"- {t}")


if __name__ == "__main__":
    main()
