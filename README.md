<!-- TOC -->
* [OpenStudioLandscapesUtil-VersionBumper](#openstudiolandscapesutil-versionbumper)
<!-- TOC -->

---

# OpenStudioLandscapesUtil-VersionBumper

```shell
putup --package VersionBumper --venv .venv --no-tox --license AGPL-3.0-or-later --force --namespace OpenStudioLandscapesUtil OpenStudioLandscapesUtil-VersionBumper
```

```shell
git remote add origin https://github.com/michimussato/OpenStudioLandscapesUtil-VersionBumper.git
git branch -M main
git push -u origin main
```

## Usage

```shell
openstudiolandscapesutil-versionbumper --old-version v1.8.0-rc1 --new-version v1.9.0-rc1 --dry-run single-file --file /home/michael/git/repos/OpenStudioLandsc
apes/pyproject.toml | grep v1.9.0
```

```shell

```