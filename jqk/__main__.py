import argparse
import json
import pkg_resources
import os
import sys

import rich.console
import rich.pretty
import rich.text


class Key:
    def __init__(self, jqkey):
        self._jqkey = jqkey

    def __repr__(self):
        return f"\033[1;34m{self._jqkey}\033[0m"


class StrData:
    def __init__(self, value):
        self._value = value

    def __repr__(self):
        return f'"{self._value}"'


def format_data(data, parent=""):
    if isinstance(data, str):
        return StrData(data)
    elif isinstance(data, list):
        if parent == "":
            parent = "."
        return [format_data(data[i], parent=f"{parent}[{i}]") for i in range(len(data))]
    elif isinstance(data, dict):
        return {
            Key(f"{parent}.{k}"): format_data(data[k], parent=f"{parent}.{k}")
            for k in data.keys()
        }
    else:
        return data


__version__ = pkg_resources.get_distribution("jqk").version


class _ShowVersionAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        print(
            "jqk {ver} at {pos}".format(
                ver=__version__, pos=os.path.dirname(os.path.dirname(__file__))
            )
        )
        parser.exit()


def main():
    parser = argparse.ArgumentParser(
        prog="jqk",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        usage="""jqk [-h] [--color-output]

jqk - Query key finder for jq [version %s]

Example:

    $ echo '{"japan": [{"name": "tokyo", "population": "14M"}, {"name": "osaka", "population": "2.7M"}]}' > data.json

    $ cat data.json | jqk
    {
      .japan: [
        {
          .japan[0].name: "tokyo",
          .japan[0].population: "14M"
        },
        {
          .japan[1].name: "osaka",
          .japan[1].population: "2.7M"
        }
      ]
    }

    $ cat data.json | jq .japan | jqk
    [
      {
        .[0].name: "tokyo",
        .[0].population: "14M"
      },
      {
        .[1].name: "osaka",
        .[1].population: "2.7M"
      }
    ]

    $ cat data.json | jq .japan[1].population -r
    2.7M
    """
        % __version__,
    )
    parser.add_argument(
        "--version",
        "-V",
        action=_ShowVersionAction,
        help="display version",
        nargs=0,
    )
    parser.add_argument(
        "--color-output",
        "-C",
        action="store_true",
        help="force color output even with pipe",
    )
    args = parser.parse_args()

    if args.color_output:
        force_terminal = True
    else:
        force_terminal = None

    if sys.stdin.isatty():
        parser.print_help()
        sys.exit(0)

    string = sys.stdin.read()

    try:
        data = json.loads(string)
    except json.decoder.JSONDecodeError as e:
        print(f"parse error: {e}", file=sys.stderr)
        sys.exit(1)

    formatted = format_data(data)

    console = rich.console.Console(
        force_terminal=force_terminal, theme=rich.theme.Theme({"repr.str": "green"})
    )
    console.print(
        rich.pretty.Pretty(
            formatted, indent_guides=False, expand_all=True, indent_size=2
        )
    )


if __name__ == "__main__":
    main()
