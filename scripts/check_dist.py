"""Validate release archive contents, metadata, and optional Git tag."""
import argparse
from email.parser import BytesParser
from pathlib import Path, PurePosixPath
import tarfile
import zipfile

try:
    import tomllib
except ModuleNotFoundError:
    try:
        import tomli as tomllib
    except ModuleNotFoundError:
        raise SystemExit(
            "Python 3.10 requires tomli for release checks. "
            "Run 'make install-dev' with the same PYTHON interpreter."
        ) from None


def check_archive(path, project):
    """Reject unexpected files and check embedded package metadata."""
    if path.suffix == '.whl':
        with zipfile.ZipFile(path) as archive:
            contents = {name: archive.read(name) for name in archive.namelist()
                        if not name.endswith('/')}
        metadata_names = [name for name in contents if name.endswith('.dist-info/METADATA')]
    else:
        with tarfile.open(path) as archive:
            contents = {str(PurePosixPath(member.name).relative_to(
                f"{project['name']}-{project['version']}")): archive.extractfile(member).read()
                        for member in archive.getmembers() if member.isfile()}
        metadata_names = ['PKG-INFO']
    for name in contents:
        parts = PurePosixPath(name).parts
        assert '..' not in parts and not name.startswith('/'), f'Unsafe path: {name}'
        allowed = (
            name in {'Makefile', 'LICENSE', 'README.md', 'CHANGELOG.md', 'RELEASE.md',
                     'requirements.txt', 'itopcli', '.itopcli.example', 'MANIFEST.in',
                     'pyproject.toml', 'setup.cfg', 'PKG-INFO'}
            or (parts[0] in {'itopcli_app', 'tests', 'scripts'} and name.endswith('.py'))
            or (parts[0] == f"{project['name']}.egg-info" and len(parts) == 2
                and parts[1] in {'PKG-INFO', 'SOURCES.txt', 'dependency_links.txt',
                                 'entry_points.txt', 'requires.txt', 'top_level.txt'})
            or (parts[0] == f"{project['name']}-{project['version']}.dist-info"
                and '/'.join(parts[1:]) in {'METADATA', 'WHEEL', 'RECORD',
                                           'entry_points.txt', 'top_level.txt',
                                           'licenses/LICENSE'})
        )
        assert allowed, f'Unexpected distribution file: {name}'
    assert len(metadata_names) == 1, 'Expected one package metadata file'
    metadata = BytesParser().parsebytes(contents[metadata_names[0]])
    assert metadata['Name'] == project['name'], 'Package name mismatch'
    assert metadata['Version'] == project['version'], 'Version mismatch'
    assert metadata['Requires-Python'] == project['requires-python'], 'Python requirement mismatch'
    assert metadata['License-Expression'] == 'MIT', 'License mismatch'
    assert 'itopcli_app/cli.py' in contents, 'Missing CLI implementation'
    print(f'{path.name}: metadata and {len(contents)} files verified')


def main():
    """Check exactly one wheel and one source archive for this version."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dist', default='dist', type=Path)
    parser.add_argument('--tag')
    args = parser.parse_args()
    project = tomllib.loads(Path('pyproject.toml').read_text())['project']
    if args.tag:
        assert args.tag == f"v{project['version']}", 'Git tag must match package version'
    expected = {f"{project['name']}-{project['version']}-py3-none-any.whl",
                f"{project['name']}-{project['version']}.tar.gz"}
    assert {path.name for path in args.dist.iterdir()} == expected, 'Unexpected or missing artifacts'
    for name in sorted(expected):
        check_archive(args.dist / name, project)


if __name__ == '__main__':
    main()
