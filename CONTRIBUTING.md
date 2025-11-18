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