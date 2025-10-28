<!-- TOC -->
* [OpenStudioLandscapesUtil-VersionBumper](#openstudiolandscapesutil-versionbumper)
  * [PyScaffold](#pyscaffold)
  * [Git](#git)
  * [Usage](#usage)
    * [Example](#example)
      * [`convert`](#convert)
      * [`yamls-to-toml`](#yamls-to-toml)
      * [`compare-tomls`](#compare-tomls)
<!-- TOC -->

---

# OpenStudioLandscapesUtil-VersionBumper

I'm trying to create a simple tool to keep the dependencies 
in each `pyproject.toml` file across the `OpenStudioLandscapes` 
project in sync.

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
usage: openstudiolandscapesutil-versionbumper [-h] [--version] [-v] [-vv] {convert,yamls-to-toml,compare-tomls} ...

A Command Line Utility for version bumping of dependencies.

positional arguments:
  {convert,yamls-to-toml,compare-tomls}

options:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -v, --verbose         set loglevel to INFO
  -vv, --very-verbose   set loglevel to DEBUG
```

### Example

#### `convert`

From `TOML` to `YAML`

```shell
# Engine
openstudiolandscapesutil-versionbumper convert --toml-in /home/michael/git/repos/OpenStudioLandscapes/pyproject.toml
```

```shell
# Features
for toml in .features/*/pyproject.toml; do 
  echo $(pwd)/${toml};
  openstudiolandscapesutil-versionbumper convert --toml-in $(pwd)/${toml}
done
```

#### `yamls-to-toml`

Write layered `yaml` files (Python `ChainMap()` to `toml`

```shell
# Engine
openstudiolandscapesutil-versionbumper yamls-to-toml \
    --root-yaml /home/michael/git/repos/OpenStudioLandscapes/utils/pyproject/pyproject.toml__OpenStudioLandscapes-Common.yaml \
    --override-yaml \
        /home/michael/git/repos/OpenStudioLandscapes/utils/pyproject/pyproject.toml__OpenStudioLandscapes-Layer-Engine.yaml \
        /home/michael/git/repos/OpenStudioLandscapes/pyproject_layer.yaml \
    --toml-out /home/michael/git/repos/OpenStudioLandscapes/pyproject.test.toml
```

```shell
# Features
for toml in .features/*/pyproject_layer.yaml; do 
  echo $(pwd)/${toml};
  openstudiolandscapesutil-versionbumper yamls-to-toml \
      --root-yaml /home/michael/git/repos/OpenStudioLandscapes/utils/pyproject/pyproject.toml__OpenStudioLandscapes-Common.yaml \
      --override-yaml \
          /home/michael/git/repos/OpenStudioLandscapes/utils/pyproject/pyproject.toml__OpenStudioLandscapes-Layer-Features.yaml \
          $(pwd)/${toml} \
      --toml-out $(dirname "$(pwd)/${toml}")/pyproject.test.toml
done
```

#### `compare-tomls`

```shell
openstudiolandscapesutil-versionbumper compare-tomls --toml-1 /home/michael/git/repos/OpenStudioLandscapes/pyproject.toml --toml-2 /home/michael/git/repos/OpenStudioLandscapes/pyproject2.toml
```