# bs4dash-py (MVP)

[![CI](https://github.com/razinkele/pydash/actions/workflows/ci.yml/badge.svg)](https://github.com/razinkele/pydash/actions/workflows/ci.yml) [Distributions (Artifacts)](https://github.com/razinkele/pydash/actions?query=workflow%3ACI) [![PyPI](https://img.shields.io/pypi/v/bs4dash-py.svg)](https://pypi.org/project/bs4dash-py/)

> Note: The PyPI badge will show the latest published version once `bs4dash-py` has been released to PyPI.

Minimal MVP to provide AdminLTE3/Bootstrap4-style dashboard building blocks for Shiny for Python.

Quick start

1. Install: `pip install -e .` (in project root)
2. Run example: `python examples/mvp_shiny.py`

Build artifacts

- The CI packaging job uploads built distributions as workflow artifacts (name: `distributions-<run_id>`).
- To download the latest wheel/sdist:
  1. Visit the CI workflow page: https://github.com/razinkele/pydash/actions/workflows/ci.yml
  2. Open the latest successful run and click **Artifacts** → download the `distributions-<run_id>` zip and extract the wheel/sdist.

Contributing

- See `CONTRIBUTING.md` for development setup, running tests and hooks.

Draft PR: scaffold and CI added
