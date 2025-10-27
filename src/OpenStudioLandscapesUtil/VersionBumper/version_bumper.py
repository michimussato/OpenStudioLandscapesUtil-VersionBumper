"""
References for pyproject.toml
    - https://packaging.python.org/en/latest/specifications/pyproject-toml/
    - https://xebia.com/blog/an-updated-guide-to-setuptools-and-pyproject-toml/
    - https://devsjc.github.io/blog/20240627-the-complete-guide-to-pyproject-toml/
"""

import argparse
import json
from collections import ChainMap
from pprint import pprint
import logging
import pathlib
import sys
from typing import Union, MutableMapping
from functools import reduce
import tomli
import tomli_w
import deepdiff

from docker_compose_graph.utils import *
from OpenStudioLandscapesUtil.VersionBumper import __version__
from OpenStudioLandscapesUtil.VersionBumper.formatter import AnsiColorFormatter

__author__ = "Michael Mussato"
__copyright__ = "Michael Mussato"
__license__ = "AGPL-3.0-or-later"

_logger = logging.getLogger(__name__)


# ---- Python API ----
# The functions defined in this section can be imported by users in their
# Python scripts/interactive interpreter, e.g. via
# `from OpenStudioLandscapesUtil.VersionBumper.skeleton import fib`,
# when using this Python module as a library.


def _recursive_serializer(obj):
    if isinstance(obj, MutableMapping):
        _recursive_serializer(obj)
    elif isinstance(obj, pathlib.PosixPath):
        return obj.as_posix()
    return str(obj)


def convert_toml_to_json(
        toml_in: pathlib.Path,
        json_out: pathlib.Path = None,
) -> pathlib.Path:

    if json_out is None:
        json_out = toml_in.with_suffix(".json")
        _logger.info(f"No output file specified. Writing to {json_out.as_posix()}...")

    json_out_edit = json_out.with_suffix(".edit.json")

    with open(toml_in, "rb") as fr:
        toml_data = tomli.load(fr)
        _logger.debug(f"Loaded {toml_data}")

    json_str = json.dumps(
        toml_data,
        indent=4,
        sort_keys=True,
    )

    with open(json_out, "w") as fw:
        _logger.info(f"Writing {json_str}")
        fw.write(json_str)

    with open(json_out_edit, "w") as fw:
        _logger.info(f"Writing {json_str}")
        fw.write(json_str)

    return json_out


def jsons_to_toml(
        root_json: pathlib.Path,
        override_json: pathlib.Path,
        toml_out: pathlib.Path,
) -> pathlib.Path:

    with open(root_json) as fr:
        _logger.debug(f"Reading {root_json.as_posix()}...")
        root_dict = json.load(fr)
        _logger.debug(f"Loaded {root_dict}")

    with open(override_json) as fr:
        _logger.debug(f"Reading {override_json.as_posix()}...")
        override_dict = json.load(fr)
        _logger.debug(f"Loaded {override_dict}")

    chain = ChainMap(
        override_dict,
        root_dict,
    )

    merged = reduce(deep_merge, chain.maps)
    _logger.debug(f"Merged chainmap: {json.dumps(merged, indent=4)}")

    toml_str = tomli_w.dumps(merged)
    _logger.debug(f"Converted TOML string: {toml_str}")

    with open(toml_out, 'w') as fw:
        _logger.debug(f"Writing {toml_out.as_posix()}")
        fw.write(toml_str)

    return toml_out


def compare_tomls(
        toml_1: pathlib.Path,
        toml_2: pathlib.Path,
):
    with open(toml_1, "rb") as fr:
        dict_1 = tomli.load(fr)

    with open(toml_2, "rb") as fr:
        dict_2 = tomli.load(fr)

    pprint(deepdiff.DeepDiff(dict_1, dict_2))


# ---- CLI ----
# The functions defined in this section are wrappers around the main Python
# API allowing them to be called directly from the terminal as a CLI
# executable/script.


def eval_(
        args: argparse.Namespace,
) -> Union[pathlib.Path]:

    _logger.debug(f"{args = }")

    _logger.debug(f"{args.processing_mode = }")

    if args.processing_mode == "convert":

        result: pathlib.Path = convert_toml_to_json(
            toml_in=args.toml_in,
            json_out=args.json_out,
        )

        _logger.info(f"{result.as_posix() = }")

        return result

    elif args.processing_mode == "jsons-to-toml":

        result: pathlib.Path = jsons_to_toml(
            root_json=args.root_json,
            override_json=args.override_json,
            toml_out=args.toml_out,
        )

        return result

    elif args.processing_mode == "compare-tomls":

        _logger.debug(f"{args.toml_1 = }")
        _logger.debug(f"{args.toml_2 = }")

        compare_tomls(
            toml_1=args.toml_1,
            toml_2=args.toml_2,
        )


def parse_args(args):
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """

    _formatter = argparse.ArgumentDefaultsHelpFormatter

    main_parser = argparse.ArgumentParser(description="A Command Line "
                                                      "Utility for version bumping "
                                                      "of dependencies.")
    main_parser.add_argument(
        "--version",
        action="version",
        version=f"OpenStudioLandscapesUtil-VersionBumper {__version__}",
    )

    main_parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        default=logging.ERROR,
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )
    main_parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )

    base_subparsers = main_parser.add_subparsers(
        dest="processing_mode",
    )

    ####################################################################################################################
    # CONVERT TOML TO JSON

    base_subparser_single_file = base_subparsers.add_parser(
        name="convert",
        formatter_class=_formatter,
    )

    base_subparser_single_file.add_argument(
        "--toml-in",
        # "-f",
        dest="toml_in",
        required=True,
        # Todo
        #  - [ ] default=pathlib.Path().cwd().joinpath(_HARBOR_DOWNLOAD_DIR, "harbor-*.tgz"),
        help="Full path to the file to be processed.",
        metavar="TOML_IN",
        type=pathlib.Path,
    )

    base_subparser_single_file.add_argument(
        "--json-out",
        # "-f",
        dest="json_out",
        required=False,
        # Todo
        #  - [ ] default=pathlib.Path().cwd().joinpath(_HARBOR_DOWNLOAD_DIR, "harbor-*.tgz"),
        help="Full path to the file to be processed.",
        metavar="JSON_OUT",
        type=pathlib.Path,
    )

    ####################################################################################################################


    ####################################################################################################################
    # JSONS TO TOML

    base_subparser_chain_dicts = base_subparsers.add_parser(
        name="jsons-to-toml",
        formatter_class=_formatter,
    )

    base_subparser_chain_dicts.add_argument(
        "--root-json",
        # "-f",
        dest="root_json",
        required=True,
        # Todo
        #  - [ ] default=pathlib.Path().cwd().joinpath(_HARBOR_DOWNLOAD_DIR, "harbor-*.tgz"),
        help="Full path to the root json.",
        metavar="ROOT_JSON",
        type=pathlib.Path,
    )

    base_subparser_chain_dicts.add_argument(
        "--override-json",
        # "-f",
        dest="override_json",
        required=True,
        # Todo
        #  - [ ] default=pathlib.Path().cwd().joinpath(_HARBOR_DOWNLOAD_DIR, "harbor-*.tgz"),
        help="Full path to the json to override the root json.",
        metavar="OVERRIDE_JSON",
        type=pathlib.Path,
    )

    base_subparser_chain_dicts.add_argument(
        "--toml-out",
        # "-f",
        dest="toml_out",
        required=True,
        # Todo
        #  - [ ] default=pathlib.Path().cwd().joinpath(_HARBOR_DOWNLOAD_DIR, "harbor-*.tgz"),
        help="Full path to the toml to be created.",
        metavar="TOML_OUT",
        type=pathlib.Path,
    )

    ####################################################################################################################


    ####################################################################################################################
    # COMPARE-TOMLS

    base_subparser_compare_tomls = base_subparsers.add_parser(
        name="compare-tomls",
        formatter_class=_formatter,
    )

    base_subparser_compare_tomls.add_argument(
        "--toml-1",
        # "-f",
        dest="toml_1",
        required=True,
        # Todo
        #  - [ ] default=pathlib.Path().cwd().joinpath(_HARBOR_DOWNLOAD_DIR, "harbor-*.tgz"),
        help="Full path to the 1st TOML.",
        metavar="TOML_1",
        type=pathlib.Path,
    )

    base_subparser_compare_tomls.add_argument(
        "--toml-2",
        # "-f",
        dest="toml_2",
        required=True,
        # Todo
        #  - [ ] default=pathlib.Path().cwd().joinpath(_HARBOR_DOWNLOAD_DIR, "harbor-*.tgz"),
        help="Full path to the 2nd TOML.",
        metavar="TOML_2",
        type=pathlib.Path,
    )

    ####################################################################################################################

    return main_parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """

    handler = logging.StreamHandler()
    handler.setLevel(loglevel)  # DEBUG INFO WARNING ERROR CRITICAL
    formatter = AnsiColorFormatter('{asctime} | {levelname:<8s} | {name:<20s} | {message}', style='{')
    handler.setFormatter(formatter)
    _logger.addHandler(handler)
    _logger.setLevel(logging.DEBUG)  # DEBUG INFO WARNING ERROR CRITICAL


def main(args):
    """Wrapper allowing :func:`fib` to be called with string arguments in a CLI fashion

    Instead of returning the value from :func:`fib`, it prints the result to the
    ``stdout`` in a nicely formatted message.

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--verbose", "42"]``).
    """
    args: argparse.Namespace = parse_args(args)
    setup_logging(args.loglevel)
    eval_(args)


def run():
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`

    This function can be used as entry point to create console scripts with setuptools.
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    # ^  This is a guard statement that will prevent the following code from
    #    being executed in the case someone imports this file instead of
    #    executing it as a script.
    #    https://docs.python.org/3/library/__main__.html

    # After installing your project with pip, users can also run your Python
    # modules as scripts via the ``-m`` flag, as defined in PEP 338::
    #
    #     python -m OpenStudioLandscapesUtil.VersionBumper.skeleton 42
    #
    run()
