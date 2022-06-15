import importlib.metadata
import re

import requests

import discapty

REG = re.compile(r"^version = \"(.*)\"")


def check_local_version_is_valid(local_version: str):
    # I hope the guy who made this regex rests in peace.
    regex = re.match(
        r"^([1-9][0-9]*!)?(0|[1-9][0-9]*)(\.(0|[1-9][0-9]*))*((a|b|rc)(0|[1-9][0-9]*))?(\.post(0|[1-9][0-9]*))?(\.dev(0|[1-9][0-9]*))?$",
        local_version,
    )
    if regex is None:
        print(f"[Valid Local] Local version is not valid: {local_version}")
        exit(1)
    print("[Valid Local] OK")


def check_pypi_version(local_version: str):
    # Get DisCapTy's version on PyPi's JSON API.
    r = requests.get("https://pypi.python.org/pypi/discapty/json")
    data = r.json()
    remote_version = data["info"]["version"]

    print(f"[PyPi] Remote version: {remote_version}")

    # See: https://docs.github.com/en/actions/using-jobs/defining-outputs-for-jobs
    print(f"::set-output name=local_version::{local_version}")
    print(f"::set-output name=remote_version::{remote_version}")

    if local_version == remote_version:
        # The local & the remote version are the same: PyPi will reject the upload
        print(
            "[PyPi] Local version and remote version are the same, the version must be updated "
            "first!"
        )
        exit(1)

    print("[PyPi] OK")


def check_local_version_against_pyproject(discapty_version: str):
    pyproject_version = importlib.metadata.version("discapty")

    print(f"[PyProject] PyProject version: {pyproject_version}")

    if discapty_version != pyproject_version:
        print("Local version and PyProject version does not match, please fix it first!")
        exit(1)

    print("[PyProject] OK")


def main():
    print("[Meta] Starting pre-release script...")

    discapty_version = discapty.__version__
    print(f"[Meta] Local version: {discapty_version}")

    check_local_version_is_valid(discapty_version)
    check_pypi_version(discapty_version)
    check_local_version_against_pyproject(discapty_version)

    print("[Meta] All checks are good, ready to deploy package at your command!")


if __name__ == "__main__":
    main()
