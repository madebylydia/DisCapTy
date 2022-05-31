import re
import requests
import os

import discapty


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
    pyproject_file = os.path.abspath(
        os.path.join(__file__, "..", "..", "pyproject.toml")
    )

    with open(pyproject_file, "r") as f:
        pyproject_version = REG.search(f.read())

        if not pyproject_version:
            raise LookupError("[PyProject] Could not find version in pyproject.toml")

        pyproject_version = pyproject_version.group(0)

        if pyproject_version != discapty_version:
            raise ValueError(
                "[PyProject] The version in pyproject.toml does not match the version in the package"
            )


def main():
    print("[Meta] Starting pre-release script...")

    discapty_version = discapty.__version__
    print("[Meta] Local version: %s", discapty_version)

    check_pypi_version(discapty_version)
    check_local_version_against_pyproject(discapty_version)

    print("[Meta] All checks are good, ready to deploy package at your command!")


if __name__ == "__main__":
    main()
