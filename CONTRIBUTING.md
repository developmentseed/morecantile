# Contributing

Issues and pull requests are more than welcome.

We recommand using [`uv`](https://docs.astral.sh/uv) as project manager for development.

See https://docs.astral.sh/uv/getting-started/installation/ for installation 

**dev install**

```bash
git clone https://github.com/developmentseed/morecantile.git
cd morecantile

uv sync --extra rasterio
```

You can then run the tests with the following command:

```sh
uv run pytest --cov morecantile --cov-report term-missing -s -vv
```

### pre-commit

This repo is set to use `pre-commit` to run *isort*, *flake8*, *pydocstring*, *black* ("uncompromising Python code formatter") and mypy when committing new code.

```bash
uv run pre-commit install
```

##### Performance tests

```sh
uv sync --group benchmark 
uv run pytest tests/benchmarks.py --benchmark-only --benchmark-columns 'min, max, mean, median' --benchmark-sort 'min'
```

### Docs

```bash
git clone https://github.com/developmentseed/morecantile.git
cd morecantile

uv sync --group docs
```

Hot-reloading docs:

```bash
uv run mkdocs serve -f docs/mkdocs.yml
```

To manually deploy docs (note you should never need to do this because Github
Actions deploys automatically for new commits.):

```bash
uv run mkdocs gh-deploy -f docs/mkdocs.yml
```

## Commit messages and releases

Releases are automated with [release-please](https://github.com/googleapis/release-please), which reads the [Conventional Commit](https://www.conventionalcommits.org/) messages merged to `main`. Use them for your commits and your PR title, e.g. `fix: handle empty collections` or `feat: add a filter option`:

- `fix:`, `perf:`, `deps:`, `revert:` and `docs:` lead to a patch release, `feat:` to a minor one, and a breaking change (`feat!:` or a `BREAKING CHANGE:` footer) to a major one.
- `chore:`, `ci:`, `test:`, `build:`, `refactor:` and `style:` don't trigger a release on their own.
- release-please keeps a release PR open with the next version; merging it tags the release and publishes it.
- CHANGES.md is written by hand: add your change under `## Unreleased`. For a breaking change, also mark the commit with `!` (e.g. `feat!:`), otherwise the release gets a patch or minor version.
- At release time, a maintainer adds the `## X.Y.Z (date)` heading under `## Unreleased`. If the version should differ from the one release-please proposes, that commit also ends with a `Release-As: X.Y.Z` line.
