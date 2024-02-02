# Getting Started


![workflow](https://github.com/fyndiq/rules-engine/actions/workflows/ci.yaml/badge.svg)
[![Downloads](https://pepy.tech/badge/rules-engine)](https://pepy.tech/project/rules-engine) ![GitHub](https://img.shields.io/github/license/fyndiq/rules-engine)

## Description

Simple rules engine inspired by [Martin Fowler's blog post in
2009](https://www.martinfowler.com/bliki/RulesEngine.html) and
[funnel-rules-engine](https://github.com/funnel-io/funnel-rules-engine).

Full source code on [github](https://github.com/fyndiq/rules-engine).

## Requirements

    python >= 3.6

## How to install

    pip install rules-engine

## How to use

```python
from rules_engine import Rule, RulesEngine, when, then

name = "fyndiq"

RulesEngine(Rule(when(name == "fyndiq"),then(True))).run(name)

>>> Result(value=True, message='it is fyndiq')

```
