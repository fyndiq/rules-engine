# Getting Started

[![CircleCI](https://circleci.com/gh/fyndiq/rules-engine.svg?style=shield)](https://circleci.com/gh/fyndiq/rules-engine) [![codecov](https://codecov.io/gh/fyndiq/rules-engine/branch/master/graph/badge.svg)](https://codecov.io/gh/fyndiq/rules-engine) [![Downloads](https://pepy.tech/badge/rules-engine)](https://pepy.tech/project/rules-engine) ![GitHub](https://img.shields.io/github/license/fyndiq/rules-engine)

## Description

Simple rules engine inspired by [Martin Fowler's blog post in
2009](https://www.martinfowler.com/bliki/RulesEngine.html) and
[funnel-rules-engine](https://github.com/funnel-io/funnel-rules-engine).

Full Documentation can be found [here](https://fyndiq.github.io/rules-engine/)

## Requirements

    python >= 3.6

## How to install

    pip install rules-engine

## How to use

```python
from rules_engine import Rule, RulesEngine, when, then

name = "fyndiq"

RulesEngine(Rule(when(name == "fyndiq"),then(True))).run(name)

>>> True
```
