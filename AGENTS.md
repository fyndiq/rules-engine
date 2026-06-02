# Agent guidelines

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

`rules-engine` is a small, dependency-free Python library for expressing business logic as condition→action rules, inspired by Martin Fowler's Rules Engine post and funnel-rules-engine. The entire implementation lives in `src/rules_engine/__init__.py` (~80 lines); everything else is tests, docs, and packaging.

## Commands

```bash
make setup        # create .venv and install requirements.txt
make test         # run pytest inside .venv
make build        # python -m build (sdist + wheel)
make publish      # twine upload dist/*
make serve-docs   # mkdocs serve (local docs preview)
make deploy-docs  # mkdocs gh-deploy

# Run a single test (activate .venv first, or use .venv/bin/pytest)
pytest tests/test_operators.py::test_any_operator
```

CI (`.github/workflows/ci.yaml`) only runs `make setup` + `make test` on push.

## Architecture

The core abstraction: a **condition is a callable** `(*args, **kwargs) -> bool` and an **action is a callable** `(*args, **kwargs) -> Any`. `RulesEngine.run(...)` passes the same args to every rule's condition and the matching rule's action. This uniform callable signature is why the combinators and helpers below all compose freely.

- `Rule(condition, action, message=None)` — pairs a condition callable with an action callable.
- `RulesEngine(*rules)` —
  - `.run(*args)` returns a `Result` for the **first** matching rule (short-circuits); raises `NoMatch` if none match.
  - `.run_all(*args)` returns a `list[Result]` for **every** matching rule; raises `NoMatch` if the list is empty.
- `Result(value, message)` — `value` is the action's return; `message` comes from the `Rule`'s `message` arg (not the action).

Helpers that build condition/action callables:
- `when(state: bool)` — wraps a *pre-evaluated* boolean into a condition (`when(x is None)` evaluates `x is None` immediately, then ignores run args). Conditions can also be plain functions of the run args (see README's `no_article_stock`).
- `then(value)` — an action that returns a constant.
- `all_(*conds)` / `any_(*conds)` / `not_(cond)` — logical combinators over condition callables.

Rule subclasses (convenience):
- `Otherwise(action)` — always-true catch-all (`when(True)`); place last.
- `NoAction(condition)` — matches but its action returns `None`.

Note actions may also raise (e.g. validation errors) rather than return a value — `run` propagates the exception.

## Conventions

- Line length 100 (black, flake8, isort all configured for it); black uses `skip_string_normalization` (single quotes preserved). flake8 ignores `W504`. mypy is configured but advisory.
- Package ships `py.typed` (PEP 561 typed). Keep public API fully type-annotated.
- Tests import from `src.rules_engine` (not the installed package). pytest config lives in `setup.cfg` (`addopts = -vv -p no:warnings`).
- Bump the version in `setup.cfg` `[metadata]` when releasing.
