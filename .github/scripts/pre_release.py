import re
import requests
import os

import discapty

import importlib.metadata

REG = re.compile(r"^version = \"(.*)\"")


def check_pypi_version(local_version: str):
    # Get DisCapTy's version on PyPi's JSON API.
    r = requests.get("https://pypi.python.org/pypi/discapty/json")
    data = r.json()
    remote_version = data["info"]["version"]

    print("[PyPi] Remote version: %s", remote_version)

    # See: https://docs.github.com/en/actions/using-jobs/defining-outputs-for-jobs
    print("::set-output name=local_version::%s", local_version)
    print("::set-output name=remote_version::%s", remote_version)

    if local_version == remote_version:
        # The local & the remote version are the same: PyPi will reject the upload
        print(
            "Local version and remote version are the same, the version must be changed first!"
        )
        exit(1)


def check_local_version_against_pyproject(discapty_version: str):
    pyproject_version = importlib.metadata.version("discapty")

    print("[PyProject] PyProject version: %s", pyproject_version)

    if discapty_version != pyproject_version:
        print(
            "Local version and PyProject version does not match, please fix it first!"
        )
        exit(1)


def main():
    print("[Meta] Starting pre-release script...")

    discapty_version = discapty.__version__
    print("[Meta] Local version: %s", discapty_version)

    check_pypi_version(discapty_version)
    check_local_version_against_pyproject(discapty_version)

    print("[Meta] All checks are good, ready to deploy package at your command!")


if __name__ == "__main__":
    main()
