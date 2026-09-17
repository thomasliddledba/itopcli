"""Upload validated distributions using tokens read as data from a local file."""
import argparse
import os
from pathlib import Path
import subprocess
import sys

REPOSITORIES = {
    'testpypi': ('TESTPYPI_API_TOKEN', 'https://test.pypi.org/legacy/'),
    'pypi': ('PYPI_API_TOKEN', 'https://upload.pypi.org/legacy/'),
}


def read_token(path, key):
    """Read a named token without evaluating shell code or exposing file contents."""
    try:
        lines = path.read_text(encoding='utf-8').splitlines()
    except (OSError, UnicodeError):
        raise ValueError('Cannot read credentials file.') from None
    values = []
    for line in lines:
        name, separator, value = line.strip().partition('=')
        if separator and name.strip() == key:
            value = value.strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
                value = value[1:-1]
            values.append(value)
    if len(values) != 1 or not values[0].startswith('pypi-') or any(
        char.isspace() for char in values[0]
    ):
        raise ValueError(f'Credentials file must contain exactly one {key}=pypi-... entry.')
    return values[0]


def main(argv=None):
    """Pass only the selected token to Twine through its subprocess environment."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('repository', choices=REPOSITORIES)
    parser.add_argument('--creds', type=Path, default=Path('.creds'))
    parser.add_argument('--verbose', action='store_true',
                        help='Show Twine diagnostics, including the server response')
    args = parser.parse_args(argv)
    key, url = REPOSITORIES[args.repository]
    try:
        token = read_token(args.creds, key)
    except ValueError as exc:
        parser.exit(2, f'{exc}\n')
    artifacts = sorted(Path('dist').glob('*.whl')) + sorted(Path('dist').glob('*.tar.gz'))
    if len(artifacts) != 2:
        parser.exit(2, 'Expected one wheel and one source archive; run make build first.\n')
    env = os.environ.copy()
    env.update(TWINE_USERNAME='__token__', TWINE_PASSWORD=token,
               TWINE_NON_INTERACTIVE='1')
    return subprocess.run(
        [sys.executable, '-m', 'twine', 'upload', '--non-interactive',
         '--repository-url', url, *(['--verbose'] if args.verbose else []),
         *map(str, artifacts)], env=env, check=False
    ).returncode


if __name__ == '__main__':
    sys.exit(main())
