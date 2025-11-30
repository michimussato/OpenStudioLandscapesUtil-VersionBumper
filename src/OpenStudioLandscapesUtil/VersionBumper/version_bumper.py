"""
References for pyproject.toml
    - https://packaging.python.org/en/latest/specifications/pyproject-toml/
    - https://xebia.com/blog/an-updated-guide-to-setuptools-and-pyproject-toml/
    - https://devsjc.github.io/blog/20240627-the-complete-guide-to-pyproject-toml/
"""

import argparse
import os
from pathlib import Path

import yaml
from collections import ChainMap
import logging
import pathlib
import sys
from typing import MutableMapping
from functools import reduce
import tomli
import tomli_w
# import deepdiff

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


def convert_toml_to_yaml(
        toml_in: pathlib.Path,
        yaml_out: pathlib.Path,
        dry_run: bool = False,
) -> pathlib.Path | None:

    if yaml_out is None:
        yaml_out = toml_in.with_suffix(".yaml")
        _logger.info(f"No output file specified. Writing to {yaml_out.as_posix()}...")

    # yaml_out_edit = yaml_out.with_suffix(".edit.yaml")

    with open(toml_in, "rb") as fr:
        toml_data = tomli.load(fr)
        _logger.debug(f"Loaded {toml_data}")

    yaml_str = yaml.safe_dump(
        toml_data,
        indent=2,
        sort_keys=True,
    )

    if dry_run:
        sys.stdout.write(yaml_str)
        return None

    with open(yaml_out, "w") as fw:
        _logger.info(f"Writing:\n{yaml_str}")
        fw.write(yaml_str)

    # with open(yaml_out_edit, "w") as fw:
    #     _logger.info(f"Writing:\n{yaml_str}")
    #     fw.write(yaml_str)

    return yaml_out


def yamls_to_toml(
        root_yaml: pathlib.Path,
        yaml_layers: list[pathlib.Path],
        toml_out: pathlib.Path,
        dry_run: bool,
) -> pathlib.Path | None:

    with open(root_yaml, "r") as fr:
        _logger.debug(f"Reading {root_yaml.as_posix()}...")
        root_dict = yaml.safe_load(stream=fr)
        _logger.debug(f"Loaded {root_dict}")

    dicts_ = []

    for f in reversed(yaml_layers):
        with open(f, "r") as fr:
            _logger.debug(f"Reading {f.as_posix()}...")
            # Todo
            #  - [ ] `safe_load_all()`? -> https://stackoverflow.com/a/70674374/2207196
            override_dict = yaml.safe_load(stream=fr)
            _logger.debug(f"Loaded {override_dict}")
            dicts_.append(override_dict)

    # remove all falsy elements
    # https://www.geeksforgeeks.org/python/remove-falsy-values-from-a-list-in-python/
    dicts = list(filter(None, dicts_))

    chain = ChainMap(
        *dicts,
        root_dict,
    )

    merged = reduce(deep_merge, chain.maps)
    _logger.debug(f"Merged chainmap:\n{yaml.safe_dump(merged, indent=2)}")

    merged_sorted = deep_sorted(merged)
    _logger.debug(f"Merged and sorted chainmap:\n{yaml.safe_dump(merged_sorted, indent=2)}")

    toml_str = tomli_w.dumps(merged_sorted)
    _logger.debug(f"Converted TOML string: {toml_str}")

    if dry_run:
        sys.stdout.write(toml_str.format(**os.environ))
        return None

    with open(toml_out, 'w') as fw:
        _logger.debug(f"Writing:\n{toml_out.as_posix()}")
        fw.write(toml_str)

    return toml_out


# def compare_tomls(
#         toml_1: pathlib.Path,
#         toml_2: pathlib.Path,
# ):
#     with open(toml_1, "rb") as fr:
#         dict_1 = tomli.load(fr)
#
#     with open(toml_2, "rb") as fr:
#         dict_2 = tomli.load(fr)
#
#     pprint(deepdiff.DeepDiff(dict_1, dict_2))


# ---- CLI ----
# The functions defined in this section are wrappers around the main Python
# API allowing them to be called directly from the terminal as a CLI
# executable/script.


def eval_(
        args: argparse.Namespace,
) -> Path | None:

    _logger.debug(f"{args = }")

    _logger.debug(f"{args.processing_mode = }")

    if args.processing_mode == "convert":

        result: pathlib.Path = convert_toml_to_yaml(
            toml_in=args.toml_in,
            yaml_out=args.yaml_out,
            dry_run=args.dry_run,
        )

        _logger.info(f"{result.as_posix() = }")

        return result

    elif args.processing_mode == "yamls-to-toml":

        result: pathlib.Path = yamls_to_toml(
            root_yaml=args.root_yaml,
            yaml_layers=args.yaml_layers,
            toml_out=args.toml_out,
            dry_run=args.dry_run,
        )

        return result

    # elif args.processing_mode == "compare-tomls":
    #
    #     _logger.debug(f"{args.toml_1 = }")
    #     _logger.debug(f"{args.toml_2 = }")
    #
    #     compare_tomls(
    #         toml_1=args.toml_1,
    #         toml_2=args.toml_2,
    #     )


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

    main_parser.add_argument(
        "--dry-run",
        dest="dry_run",
        action="store_true",
        required=False,
        default=False,
        help="Just print, don't write anything.",
    )

    base_subparsers = main_parser.add_subparsers(
        dest="processing_mode",
    )

    ####################################################################################################################
    # CONVERT TOML TO YAML

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
        "--yaml-out",
        # "-f",
        dest="yaml_out",
        required=False,
        default=None,
        # Todo
        #  - [ ] default=pathlib.Path().cwd().joinpath(_HARBOR_DOWNLOAD_DIR, "harbor-*.tgz"),
        help="Full path to the file to be processed.",
        metavar="YAML_OUT",
        type=pathlib.Path,
    )

    ####################################################################################################################


    ####################################################################################################################
    # YAMLS TO TOML

    base_subparser_chain_dicts = base_subparsers.add_parser(
        name="yamls-to-toml",
        formatter_class=_formatter,
    )

    base_subparser_chain_dicts.add_argument(
        "--root-yaml",
        # "-f",
        dest="root_yaml",
        required=True,
        # Todo
        #  - [ ] default=pathlib.Path().cwd().joinpath(_HARBOR_DOWNLOAD_DIR, "harbor-*.tgz"),
        help="Full path to the root layer YAML.",
        metavar="ROOT_YAML",
        type=pathlib.Path,
    )

    base_subparser_chain_dicts.add_argument(
        "--yaml-layers",
        # "-f",
        dest="yaml_layers",
        nargs="*",
        required=True,
        # Todo
        #  - [ ] default=pathlib.Path().cwd().joinpath(_HARBOR_DOWNLOAD_DIR, "harbor-*.tgz"),
        help="Full path(s) to the YAML layer(s). "
             "The latter will take precendence over the former.",
        metavar="YAML_LAYERS",
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


    # ####################################################################################################################
    # # COMPARE-TOMLS
    #
    # base_subparser_compare_tomls = base_subparsers.add_parser(
    #     name="compare-tomls",
    #     formatter_class=_formatter,
    # )
    #
    # base_subparser_compare_tomls.add_argument(
    #     "--toml-1",
    #     # "-f",
    #     dest="toml_1",
    #     required=True,
    #     # Todo
    #     #  - [ ] default=pathlib.Path().cwd().joinpath(_HARBOR_DOWNLOAD_DIR, "harbor-*.tgz"),
    #     help="Full path to the 1st TOML.",
    #     metavar="TOML_1",
    #     type=pathlib.Path,
    # )
    #
    # base_subparser_compare_tomls.add_argument(
    #     "--toml-2",
    #     # "-f",
    #     dest="toml_2",
    #     required=True,
    #     # Todo
    #     #  - [ ] default=pathlib.Path().cwd().joinpath(_HARBOR_DOWNLOAD_DIR, "harbor-*.tgz"),
    #     help="Full path to the 2nd TOML.",
    #     metavar="TOML_2",
    #     type=pathlib.Path,
    # )
    #
    # ####################################################################################################################

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
