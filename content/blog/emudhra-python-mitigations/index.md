---
# Generated from the Obsidian vault by scripts/vault_export.py. Edit the note there.
title: eMudhra Python mitigations
date: 2026-10-23T14:37:18-07:00
tags: []
draft: false
slug: emudhra-python
---

The [eMudhra problem](https://emudhra.we-have-a-problem.com/) is quite bad. Any system that depends on TLS/SSL and makes network requests is potentially vulnerable. eMudhra was added in spring 2019, so most versions of until 2026-10-20 have problems.

Examples of things in need of attention:

- any Linux machines with old cron jobs/services making network requests
- old Docker images deployed somewhere
- CI package caches
- Python venvs with the `certifi` dependency or with the `pip` dependency (which vendors its own certificates)

For Python specifically, you'll need to update `pip` and `uv`, since they vendor their own certs and those are exposed. 

```sh
# Update uv
brew update && brew upgrade uv
# or
sudo pacman -Sy uv
# or
uv self update
# Upgrade all Python installations which now ship a patched pip
uv python upgrade

# Updating pip
python -m pip install "pip @ https://files.pythonhosted.org/packages/3f/06/3e4420302363fbb71be3c7f35ce042f54bfca330e3e66b3a2e3c4cca579f/pip-26.2.2-py3-none-any.whl#sha256=fd7f4dfa8190e014013b9f08f3e973f4e4c26ffd179a204895533a7254813a70"
```

More useful scripts and information here: [Information for Python users regarding eMudhra / emSign CA certificate security incident - Announcements - Discussions on Python.org](https://discuss.python.org/t/information-for-python-users-regarding-emudhra-emsign-ca-certificate-security-incident/109576).

Any vulnerable venv needs to upgrade

```sh
# Upgrade certifi and pip
uv pip install -U certifi pip
# If a uv.lock is present, it needs an explicit version bump
uv lock --upgrade-package certifi
```

This script will find and print all Python venvs on your machine (under your user) and print the `certifi` version in that venv

```sh
find ~ /opt /usr/lib -xdev -type f -path '*certifi/__init__.py' 2>/dev/null |
while read f; do
  v=$(grep -m1 -oP '__version__ = "\K[^"]+' "$f")
  echo "$v  ${f%/__init__.py}"
done | sort
```
