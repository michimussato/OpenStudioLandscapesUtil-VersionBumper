"""
This is a skeleton file that can serve as a starting point for a Python
console script. To run this script uncomment the following lines in the
``[options.entry_points]`` section in ``setup.cfg``::

    console_scripts =
         fibonacci = VersionBumper.skeleton:run

Then run ``pip install .`` (or ``pip install -e .`` for editable mode)
which will install the command ``fibonacci`` inside your current environment.

Besides console scripts, the header (i.e. until ``_logger``...) of this file can
also be used as template for Python modules.

Note:
    This file can be renamed depending on your needs or safely removed if not needed.

References:
    - https://setuptools.pypa.io/en/latest/userguide/entry_point.html
    - https://pip.pypa.io/en/stable/reference/pip_install
"""

import argparse
from pprint import pprint
import logging
import pathlib
import sys
from typing import Union, MutableMapping

from OpenStudioLandscapesUtil.VersionBumper import __version__

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
    return obj


def bump_version(
        old_version: str,
        new_version: str,
        file_path: pathlib.Path,
        dry_run: bool,
) -> MutableMapping[str, Union[pathlib.Path, str]]:
    # Read in the file
    with open(file_path, 'r') as fr:
      file_data = fr.read()

    # Replace the target string
    file_data = file_data.replace(
        old_version,
        new_version,
    )

    # Write the file out again
    if not dry_run:
        with open(file_path, 'w') as fw:
          fw.write(file_data)

    return {
        "file_path": file_path,
        "file_data": file_data,
    }


# ---- CLI ----
# The functions defined in this section are wrappers around the main Python
# API allowing them to be called directly from the terminal as a CLI
# executable/script.


def eval_(
        args: argparse.Namespace,
) -> Union[pathlib.Path]:

    _logger.debug(f"{args = }")

    _logger.debug(f"{args.processing_mode = }")

    # dotenv_ = args.dot_env
    #
    # if dotenv_ is not None:
    #     dotenv_: pathlib.Path = args.dot_env.expanduser().resolve()
    #     if not dotenv_.exists():
    #         raise FileNotFoundError(f"{dotenv_.as_posix()} does not exist")
    #
    # load_dotenv(
    #     dotenv_path=dotenv_,
    #     verbose=True,
    # )

    if args.processing_mode == "single-file":
        # _logger.debug(f"{args.processing_mode = }")

        ret: MutableMapping[str, Union[pathlib.Path, str]] = bump_version(
            old_version=args.old_version,
            new_version=args.new_version,
            file_path=args.file_path,
            dry_run=args.dry_run,
        )

        pprint(ret)

        # sys.stdout.write(
        #     "%s" % json.dumps(
        #         obj=ret,
        #         default=recursive_serializer,
        #         indent=4,
        #         sort_keys=True,
        #     )
        # )



        # if args.prepare_command == "download":
        #     result: pathlib.Path = _cli_download(args)
        #     _logger.debug(f"{result = }")
        #     return result
        #
        # elif args.prepare_command == "extract":
        #     result: pathlib.Path = _cli_extract(args)
        #     _logger.debug(f"{result = }")
        #     return result
        #
        # elif args.prepare_command == "configure":
        #     if args.dry_run:
        #         # from pprint import pprint
        #         print(_configure(args))
        #         return None
        #     else:
        #         result = _cli_configure(args)
        #         _logger.debug(f"{result = }")
        #         return result
        #
        # elif args.prepare_command == "install":
        #     result: subprocess.CompletedProcess = _cli_install(args)
        #     _logger.debug(f"{result = }")
        #     return result

    elif args.processing_mode == "multi-file":

        _logger.debug(f"{args.root_path = }")
        _logger.debug(f"{args.pattern = }")

        exclude = [
            "__pycache__",
            ".idea",
            ".teleport",
            ".bom",
            ".pi-hole",
            ".git",
            "tests",
            ".dagster",
            ".pytest_cache",
            ".payload",
            ".harbor",
            ".dagster-postgres",
            ".portainer",
            "obsidian",
            ".venv",
            ".nox",
            ".landscapes"
        ]

        for f in args.root_path.glob(f"**/{args.pattern}"):
            if bool(list(set(f.parts) & set(exclude))):
                continue

            print(f)

            ret: MutableMapping[str, Union[pathlib.Path, str]] = bump_version(
                old_version=args.old_version,
                new_version=args.new_version,
                file_path=f,
                dry_run=args.dry_run,
            )

            pprint(ret)

        # _logger.debug(f"{configfiles = }")
        #
        # for file_path in configfiles:
        #
        #     ret: MutableMapping[str, Union[pathlib.Path, str]] = bump_version(
        #         old_version=args.old_version,
        #         new_version=args.new_version,
        #         file_path=pathlib.Path(file_path),
        #         dry_run=args.dry_run,
        #     )
        #
        #     # pprint(ret)

        # pass
        # _logger.debug(f"{args.systemd_command = }")

        # if args.systemd_command == "install":
        #     result: list = _cli_systemd_install(args)
        #     _logger.debug(f"{result = }")
        #     return result
        #
        # elif args.systemd_command == "uninstall":
        #     result: list = _cli_systemd_uninstall(args)
        #     _logger.debug(f"{result = }")
        #     return result
        #
        # elif args.systemd_command == "status":
        #     result: list = _cli_systemd_status()
        #     _logger.debug(f"{result = }")
        #     return result
        #
        # elif args.systemd_command == "journalctl":
        #     result: list = _cli_systemd_journalctl()
        #     _logger.debug(f"{result = }")
        #     return result

    # elif args.command == "project":
    #     _logger.debug(f"{args.project_command = }")
    #
    #     if args.project_command == "create":
    #         result: list = _cli_project_create(args)
    #         _logger.debug(f"{result = }")
    #         return result
    #
    #     if args.project_command == "delete":
    #         result: list = _cli_project_delete(args)
    #         _logger.debug(f"{result = }")
    #         return result


def parse_args(args):
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """

    _formatter = argparse.ArgumentDefaultsHelpFormatter

    main_parser = argparse.ArgumentParser(description="Just a Fibonacci demonstration")
    main_parser.add_argument(
        "--version",
        action="version",
        version=f"OpenStudioLandscapesUtil-VersionBumper {__version__}",
    )

    main_parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
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
        "--old-version",
        # "-h",
        dest="old_version",
        required=True,
        default=None,
        help="The version str to search for, "
             "i.e. `v1.2.3-rc1`.",
        metavar="OLD_VERSION",
        type=str,
    )

    main_parser.add_argument(
        "--new-version",
        # "-h",
        dest="new_version",
        required=True,
        default=None,
        help="The version str to apply, "
             "i.e. `v1.2.3-rc1`.",
        metavar="NEW_VERSION",
        type=str,
    )

    main_parser.add_argument(
        "--dry-run",
        dest="dry_run",
        action="store_true",
        required=False,
        default=False,
        help="Just print, don't do.",
    )

    base_subparsers = main_parser.add_subparsers(
        dest="processing_mode",
    )

    ####################################################################################################################
    # SINGLE-FILE

    base_subparser_single_file = base_subparsers.add_parser(
        name="single-file",
        formatter_class=_formatter,
    )

    base_subparser_single_file.add_argument(
        "--file-path",
        # "-f",
        dest="file_path",
        required=True,
        # Todo
        #  - [ ] default=pathlib.Path().cwd().joinpath(_HARBOR_DOWNLOAD_DIR, "harbor-*.tgz"),
        help="Full path to the file to be processed.",
        metavar="FILE_PATH",
        type=pathlib.Path,
    )

    ####################################################################################################################


    ####################################################################################################################
    # MULTI-FILE

    base_subparser_single_file = base_subparsers.add_parser(
        name="multi-file",
        formatter_class=_formatter,
    )

    base_subparser_single_file.add_argument(
        "--root-path",
        # "-f",
        dest="root_path",
        required=True,
        # Todo
        #  - [ ] default=pathlib.Path().cwd().joinpath(_HARBOR_DOWNLOAD_DIR, "harbor-*.tgz"),
        help="Full path to the file to be processed.",
        metavar="ROOT_PATH",
        type=pathlib.Path,
    )

    base_subparser_single_file.add_argument(
        "--pattern",
        # "-f",
        dest="pattern",
        required=True,
        # Todo
        #  - [ ] default=pathlib.Path().cwd().joinpath(_HARBOR_DOWNLOAD_DIR, "harbor-*.tgz"),
        help="Full path to the file to be processed.",
        metavar="PATTERN",
        type=str,
    )

    ####################################################################################################################

    return main_parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )


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
