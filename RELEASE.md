# Publishing itopcli 0.1.0

The package and installed command are named `itopcli`. Version `0.1.0` is
specified in `pyproject.toml`. The source launcher remains `./itopcli`.
Preparing these files does not publish a release.

## Local publishing with Make

Use GNU Make and Python 3.10+ in an activated virtual environment:

```bash
make install-dev
make check
make build
```

Append these named entries to your local `.creds` file, replacing the placeholders
with separate API tokens from each index:

```text
TESTPYPI_API_TOKEN=pypi-REPLACE_WITH_TESTPYPI_TOKEN
PYPI_API_TOKEN=pypi-REPLACE_WITH_PYPI_TOKEN
```

Optional matching single or double quotes around a token are accepted. Other
lines are ignored. This file is read as data, never executed as shell code.
Keep `.creds` private (for example, `chmod 600 .creds` on Linux/macOS); it remains
ignored by Git and excluded from distributions. The helper passes the selected
token to Twine through the subprocess environment, not command-line arguments.

```bash
make publish-testpypi
# Verify the TestPyPI installation before publishing the same artifacts:
make publish-pypi
```

If an upload fails with a generic HTTP error, enable Twine's response diagnostics:

```bash
make publish-testpypi VERBOSE=1
```

This retries the upload; it is not a dry run. Read the server response before
changing the version or credentials. Local metadata validation does not check
whether an index will accept a filename, version, or project name.

Both publish targets validate existing files in `dist/` and then upload them.
They do not rebuild or skip existing versions. Run `make build` again after
source changes. `make clean` removes only `build/`, `dist/`, and
`itopcli.egg-info/`; use it before building a new version to remove stale artifacts.

Use `make help` to list targets. Override the interpreter or credentials path with
`make publish-testpypi PYTHON=.venv/bin/python CREDS=/path/to/.creds`.
`make build BUILD_FLAGS=--no-isolation` is available when the build requirements
are already installed. Account tokens are an alternative to the GitHub Trusted
Publishing workflow below; local publishing does not require that workflow setup.

## One-time setup

1. Sign in to [PyPI](https://pypi.org/) and [TestPyPI](https://test.pypi.org/)
   with verified email and two-factor authentication. They use separate accounts.
2. Confirm that you can publish under the name `itopcli`. A missing project page
   does not guarantee that a name is available. If the name is already owned by
   someone else, choose another distribution name before releasing.
3. In the GitHub repository, create environments named `testpypi` and `pypi`.
   Configure the production environment to allow release tags (`v*`). Required
   reviewers can be added if you want a manual release gate.
4. Add a pending publisher on each index's account Publishing page:
   [PyPI](https://pypi.org/manage/account/publishing/) and
   [TestPyPI](https://test.pypi.org/manage/account/publishing/).

   | Setting | PyPI | TestPyPI |
   | --- | --- | --- |
   | Project name | `itopcli` | `itopcli` |
   | GitHub owner | `thomasliddledba` | `thomasliddledba` |
   | Repository | `itopcli` | `itopcli` |
   | Workflow filename | `release.yml` | `release.yml` |
   | Environment | `pypi` | `testpypi` |

   If you already own the project, add the publisher in that project's Publishing
   settings instead. No long-lived PyPI token or GitHub secret is needed.
   See [PyPI's pending publisher instructions](https://docs.pypi.org/trusted-publishers/creating-a-project-through-oidc/).

## Build and review locally

Use Python 3.10 or newer for release tooling. `make install-dev` includes the
`tomli` TOML parser on Python 3.10; newer versions use the standard library.
Run from a clean checkout in a virtual environment:

```bash
python -m pip install -e '.[dev]'
python -m build
python -m twine check --strict dist/*
python scripts/check_dist.py --tag v0.1.0
```

Use an empty `dist/` directory for each release. The checker rejects extra
artifacts, unexpected archive paths, and mismatched name/version metadata.
The source archive includes the placeholder `.itopcli.example`, tests, and
release instructions. Neither archive should contain `.itopcli`, `.creds`,
virtual environments, or the local iTop installation.

`python -m build` builds the wheel from the source archive, checking that the
source distribution contains the files needed to build independently.
Install the wheel in a fresh environment and run the tests from outside the
checkout to ensure Python imports the installed package:

```bash
python -m venv /tmp/itopcli-release-check
/tmp/itopcli-release-check/bin/python -m pip install dist/itopcli-0.1.0-py3-none-any.whl
cd /tmp
/tmp/itopcli-release-check/bin/python -m unittest discover -s /absolute/path/to/itopcli/tests -v
/tmp/itopcli-release-check/bin/itopcli --help
/tmp/itopcli-release-check/bin/python -m pip check
```

The example above uses POSIX paths; on Windows use the environment's `Scripts`
directory. Review the changelog and wait for Linux/Windows CI to pass.

## Rehearse on TestPyPI

Push the reviewed commit and workflow to GitHub. Under Actions → Release → Run
workflow, select that commit's branch or tag and leave `target` as `testpypi`.
The workflow runs CI before building and publishing. TestPyPI versions, like
PyPI versions, cannot simply be overwritten; use a new version for a changed
artifact after an upload.

Test the result in a fresh environment. Install runtime dependencies from PyPI,
then fetch only itopcli from TestPyPI, so dependency resolution does not mix indexes:

```bash
python -m pip install -r requirements.txt
python -m pip install --index-url https://test.pypi.org/simple/ --no-deps itopcli==0.1.0
itopcli --help
itopcli query --class Server --dry-run
python -m pip check
```

This tests CLI installation without contacting an iTop server.

## Publish on PyPI

1. Commit the reviewed release files and complete the project's normal review.
2. Create and push tag `v0.1.0` on the reviewed commit.
3. Publish a GitHub release for `v0.1.0`, using the changelog as release notes.
   **Publishing the GitHub release starts the production publishing workflow.**
   Alternatively, manually run Release on tag `v0.1.0` with target `pypi`.
   Use one trigger, not both, to avoid attempting a duplicate upload.
4. The workflow reruns CI, validates the version/tag, builds and checks artifacts,
   tests the installed wheel, and uploads via the `pypi` environment.
5. Verify the project page and installation in a fresh environment:

   ```bash
   python -m pip install itopcli==0.1.0
   itopcli --help
   ```

An upload publishes a version permanently; fixes need a new version and tag.
Future releases update `pyproject.toml` and `CHANGELOG.md` together.

Reference: [PyPA's GitHub Actions publishing guide](https://packaging.python.org/en/latest/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/).
