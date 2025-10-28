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

The idea is to create `pyproject.toml` files based on a layered structure:

Todo: find a more appropriate name for `override` (in fact, it's an overlay).

```
# Bottom up
-----------------
= Resulting TOML
-----------------
+ override-yaml-n
+ overrice-yaml-2
+ override-yaml-1
root-layer-yaml
```

The process is always additive, never subtractive (at least for the time being).

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
mv --backup=numbered ~/git/repos/OpenStudioLandscapes/pyproject.toml ~/git/repos/OpenStudioLandscapes/pyproject.bak.toml

openstudiolandscapesutil-versionbumper yamls-to-toml \
    --root-yaml ~/git/repos/OpenStudioLandscapes/pyproject_layers/pyproject_layer_0_root.yaml \
    --override-yaml \
        ~/git/repos/OpenStudioLandscapes/pyproject_layers/pyproject_layer_engine.yaml \
        ~/git/repos/OpenStudioLandscapes/pyproject_layer.yaml \
    --toml-out ~/git/repos/OpenStudioLandscapes/pyproject.toml
```

```shell
# Features
pushd .features || exit 1
for toml in */pyproject_layer.yaml; do
  _toml=$(pwd)/${toml}
  cwd=$(dirname ${_toml})
  pushd ${cwd} || exit 1
  openstudiolandscapesutil-versionbumper yamls-to-toml \
      --root-yaml ~/git/repos/OpenStudioLandscapes/pyproject_layers/pyproject_layer_0_root.yaml \
      --override-yaml \
          ~/git/repos/OpenStudioLandscapes/pyproject_layers/pyproject_layer_features.yaml \
          "${_toml}" \
      --toml-out "${cwd}/pyproject.toml"
  popd || exit 1
done
popd || exit 1
```
