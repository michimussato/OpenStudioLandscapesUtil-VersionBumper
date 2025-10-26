<!-- TOC -->
* [OpenStudioLandscapesUtil-VersionBumper](#openstudiolandscapesutil-versionbumper)
  * [PyScaffold](#pyscaffold)
  * [Git](#git)
  * [Usage](#usage)
    * [Example](#example)
      * [`single-file` Mode](#single-file-mode)
      * [`multi-file` Mode](#multi-file-mode)
        * [`pyproject.toml`](#pyprojecttoml)
        * [`README.md`](#readmemd)
<!-- TOC -->

---

# OpenStudioLandscapesUtil-VersionBumper

I'm trying to create a simple tool to keep the dependencies 
in each `pyproject.toml` file across the `OpenStudioLandscapes` 
project in sync. Mainly, the challenges are to filter for the correct list of 
files as well as to avoid ambiguous string replacements replace like:
- `v1.0.0-rc1` -> `v1.0.1-rc1-rc1`.

This is a first attempt and far from perfect. However, aware of its current
pitfalls, let's see to what extent it is useful in its current state.

## PyScaffold

The package was created using the following `PyScaffold` command:

```shell
putup --package VersionBumper --venv .venv --no-tox --license AGPL-3.0-or-later --force --namespace OpenStudioLandscapesUtil OpenStudioLandscapesUtil-VersionBumper
```

## Git

And then pushed to a new Git repo using:

```shell
git remote add origin https://github.com/michimussato/OpenStudioLandscapesUtil-VersionBumper.git
git branch -M main
git push -u origin main
```

## Usage

```
$ openstudiolandscapesutil-versionbumper --help
usage: openstudiolandscapesutil-versionbumper [-h] [--version] [-v] [-vv] --old-version OLD_VERSION --new-version NEW_VERSION [--dry-run] {single-file,multi-file} ...

A Command Line Utility for version bumping of dependencies.

positional arguments:
  {single-file,multi-file}

options:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -v, --verbose         set loglevel to INFO
  -vv, --very-verbose   set loglevel to DEBUG
  --old-version OLD_VERSION
                        The version str to search for, i.e. `v1.2.3-rc1`.
  --new-version NEW_VERSION
                        The version str to apply, i.e. `v1.2.3-rc1`.
  --dry-run             Just print, don't do
```

### Example

#### `single-file` Mode

```shell
openstudiolandscapesutil-versionbumper --old-version v1.8.0-rc1 --new-version v1.9.0-rc1 --dry-run single-file --file /home/michael/git/repos/OpenStudioLandscapes/pyproject.toml | grep v1.9.0
```

#### `multi-file` Mode

##### `pyproject.toml`

```shell
openstudiolandscapesutil-versionbumper -vv --old-version v1.8.0-rc1 --new-version v1.9.0-rc1 --dry-run multi-file --root-path /home/michael/git/repos/OpenStudioLandscapes --pattern pyproject.toml | grep v1.9.0
```

##### `README.md`

```shell
openstudiolandscapesutil-versionbumper -vv --old-version v1.8.0-rc1 --new-version v1.9.0-rc1 --dry-run multi-file --root-path /home/michael/git/repos/OpenStudioLandscapes --pattern README.md | grep v1.9.0
```
