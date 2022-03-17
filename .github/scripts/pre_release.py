import discapty
import requests

def main():
    print('Starting pre-release script...')

    # Get information about the current code's version
    local_version = discapty.__version__
    print('Local version: %s', local_version)
    
    # Get DisCapTy's version on PyPi's JSON API.
    r = requests.get('https://pypi.python.org/pypi/discapty/json')
    data = r.json()
    remote_version = data['info']['version']

    print('Remote version: %s', remote_version)

    # See: https://docs.github.com/en/actions/using-jobs/defining-outputs-for-jobs
    print("::set-output name=local_version::%s", local_version)
    print("::set-output name=remote_version::%s", remote_version)

    if local_version == remote_version:
        # The local & the remote version are the same: PyPi will reject the upload
        print('Local version and remote version are the same, the version must be changed first!')
        exit(1)

    print('All checks are good, ready to deploy package at your command!')

if __name__ == '__main__':
    main()
