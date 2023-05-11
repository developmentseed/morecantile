# Contributing

Issues and pull requests are more than welcome.

**dev install**

```bash
$ git clone https://github.com/developmentseed/morecantile.git
$ cd morecantile
$ python -m pip install -e .["dev"]
```

You can then run the tests with the following command:

```sh
python -m pytest --cov morecantile --cov-report term-missing -s -vv
```

### pre-commit

This repo is set to use `pre-commit` to run *isort*, *flake8*, *pydocstring*, *black* ("uncompromising Python code formatter") and mypy when committing new code.

```bash
$ pre-commit install
```

### Docs

```bash
$ git clone https://github.com/developmentseed/morecantile.git
$ cd morecantile
$ python -m pip install -e .["docs"]
```

Hot-reloading docs:

```bash
$ mkdocs serve -f docs/mkdocs.yml
```

To manually deploy docs (note you should never need to do this because Github
Actions deploys automatically for new commits.):

```bash
$ mkdocs gh-deploy -f docs/mkdocs.yml
```
