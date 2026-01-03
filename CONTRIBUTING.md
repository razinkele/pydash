# Contributing to bs4dash-py

Thanks for considering contributing! Please follow these guidelines:

- Fork the repository and create a feature branch (e.g., `feature/my-component`).
- Run the test suite locally: `pip install -e '.[dev]'` then `pytest -q`.
- Run pre-commit hooks and formatting: `pre-commit install` then `pre-commit run --all-files`.
- Keep changes focused and open a PR against `main` with a clear description and changelog entry.

For large features, open an issue first to discuss design.

Requesting a gallery preview

- To request a visual preview of your PR (screenshots/thumbnails), add the `preview` label to the pull request.
  - In the GitHub UI: open the PR, click **Labels**, and select **preview**.
  - With the GitHub CLI: `gh pr edit <number> -l preview`.
- The CI job will run a best-effort capture that generates thumbnails and uploads them as an artifact on the PR. This is non-blocking and intended to help reviewers preview UI changes quickly.

See `docs/ci-flakiness.md` for guidance on dealing with CI flakiness (timeouts, Playwright/browser installs, and diagnostic tips).
