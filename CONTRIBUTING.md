# Contributing to itopcli

Contributions are welcome through GitHub pull requests. This guide covers setting
up a development environment, checking changes, and submitting them for review.
For CLI installation and usage, see [README.md](README.md).

## Report bugs and propose improvements

Use the [issue tracker](https://github.com/thomasliddledba/itopcli/issues) for
itopcli bugs, feature requests, and questions. Report issues with other tools to
those projects' issue trackers.

For a bug report, include the command you ran, the expected and actual results,
your operating system, Python and itopcli versions, and the iTop version when
relevant. Remove passwords, API tokens, and private configuration values from
examples and logs.

For a feature proposal, describe the use case and the expected CLI behavior.
The current roadmap includes:

- Lookup helpers to resolve names to IDs.
- Workflow support through `apply_stimulus`.
- Relationship management.

## Set up a development environment

Use Python 3.10 or newer. Fork the repository on GitHub, clone your fork, and
create a feature branch:

```bash
git clone https://github.com/YOUR-USERNAME/itopcli.git
cd itopcli
git switch -c describe-your-change
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
```

On Windows, create the environment with `python -m venv .venv` and activate it
with `.venv\Scripts\Activate.ps1` in PowerShell. The editable installation makes
source changes available to the installed `itopcli` command. The `./itopcli`
launcher also works from the checkout.

With GNU Make installed, `make install-dev` installs the same development and
release dependencies. Use `make help` to list available commands. Override the
interpreter when necessary, for example `make test PYTHON=.venv/bin/python`.

## Run tests and checks

Run these checks from the repository root in your activated environment:

| Task | Make command | Python command |
| --- | --- | --- |
| Regression tests | `make test` | `python -m unittest discover -s tests -v` |
| Lint | `make lint` | `python -m pylint --fail-under=9.5 itopcli_app/cli.py itopcli` |
| Tests and lint | `make check` | Run both commands above |
| Build and validate archives | `make build` | See the build steps below |
| Check existing archives | `make check-dist` | Run the two validation commands below |

To build and validate without Make:

```bash
python -m build
python scripts/check_dist.py
python -m twine check --strict dist/*
```

Tests use temporary configuration files and mocked HTTP requests; they do not
contact an iTop server. CI covers Python 3.10–3.14 on Linux and Windows and checks
installation and the installed command. Push and pull request CI runs only when
application code, tests, scripts, packaging files, the Makefile, the example
configuration, or workflow definitions change. Documentation-only changes skip
these runs. Release publishing still invokes the full CI checks explicitly.
Live compatibility with an iTop data
model requires separate integration testing. Describe any integration testing
in your pull request, including the iTop version tested.

Use pylint's default rules without a project-specific configuration file. The
minimum score is 9.5/10. Add or update regression tests for behavior changes and
bug fixes. Documentation-only changes should be checked for accurate commands,
working links, and readable formatting.

## Prepare a pull request

1. Keep each pull request focused on one change; submit unrelated changes separately.
2. Update the README's usage examples when adding or changing user-facing behavior.
3. When reusing third-party code, preserve required attribution and update the
   README's Acknowledgements section as appropriate.
4. Run the relevant tests and lint checks. For packaging changes, also build and
   validate the release archives.
5. Commit your changes, push your feature branch to your fork, and open a pull
   request against this repository.

Explain the problem, what changed, and how you verified it. Link related issues
and mention any remaining limitations. Keep local credentials such as `.itopcli`
and `.creds` out of commits and pull request output.

## Review and merge

A maintainer reviews each pull request and the CI results. Address review feedback
and resolve failing checks before merging. At least one maintainer must approve
the change with “LGTM” (Looks Good To Me) or an equivalent approval before the
pull request can be merged.

## Releases

Release maintainers should follow [RELEASE.md](RELEASE.md) for version handling,
archive validation, TestPyPI installation testing, and publishing. The Makefile
provides `make publish-testpypi` and `make publish-pypi` for token-based uploads;
GitHub Actions also supports Trusted Publishing. Publishing is separate from
contributor setup and testing.
