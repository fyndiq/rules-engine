# Getting Started

![workflow](https://github.com/fyndiq/rules-engine/actions/workflows/ci.yaml/badge.svg)
[![Downloads](https://pepy.tech/badge/rules-engine)](https://pepy.tech/project/rules-engine) ![GitHub](https://img.shields.io/github/license/fyndiq/rules-engine)

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

## When

Evaluates a condition.

let's check if a value is `None` and raise an exception.

```python

from rules_engine import Rule, RulesEngine, when
obj = None

def cannot_be_none_error():
    return "not a string error"

RulesEngine(Rule(when(obj is None), cannot_be_none_error)).run(obj)

>>> 'not a string error'
```

## Then

Evaluates an action.

```python

from rules_engine import Rule, RulesEngine, when
obj = None

RulesEngine(Rule(when(obj is None), then('not a string error'))).run(obj)

>>> 'not a string error'
```

## Not

The `not_` keyword is a logical operator.

The return value will be `True` if the statement(s) are not `True`, otherwise it will return `False`.


```python

from rules_engine import Rule, RulesEngine, not_

def is_missing(obj):
    return not obj

obj="Hello"

RulesEngine(Rule(not_(is_missing), then(True))).run(obj)

>>> True
```

## All

Evaluates multiple conditions and if all conditions are `True` the action is executed

- Example:
    - We need to check if an object `obj` is not missing and is of type `list`


```python

from rules_engine import Rule, RulesEngine, all_

def is_missing(obj):
    return not obj

def is_a_list(obj):
    return isinstance(obj, list)

obj = [1,2]

RulesEngine(Rule(all_(not_(is_missing), is_a_list), then(True))).run(obj)

>>> True
```

## Any

Evaluates multiple conditions and if any of the conditions is `True` the action is executed

- Example:
    - We need to check if an object `obj` is a `str` or a `list`


```python

from rules_engine import Rule, RulesEngine, any_

def is_a_str(obj):
    return isinstance(obj, str)

def is_a_list(obj):
    return isinstance(obj, list)

obj = "Hello"

RulesEngine(Rule(any_(is_a_str, is_a_list), then(True))).run(obj)

>>> True
```

## Run/RunAll

### Run

Runs rules sequentially and exists executes the action for the first passing condition.

```python

from rules_engine import Rule, RulesEngine, them
obj = None

def is_integer(value):
    return isinstance(value, int)


def is_string(value):
   return isinstance(value, str)


value=1234
RulesEngine(
      Rule(is_integer, then("integer")),
      Rule(is_string, then("string")),
      ).run(value)

>>> "integer"
```

Since the first rule satisfies the conditions the rules engine will go no further

### RunAll

Evaluates all conditions and adds them to a list

```python
from rules_engine import Rule, RulesEngine, then

def is_integer(value):
    return isinstance(value, int)


def is_string(value):
   return isinstance(value, str)

def is_gr_3_chars(value):
   return len(value) > 3



value="Hello"
RulesEngine(
      Rule(is_integer, then("integer")),
      Rule(is_string, then("string")),
      Rule(is_gr_3_chars, then("greater than 3 charcters")),
      ).run_all(value)

>>> ["string", "greater than 3 charcters"]

```

# Full Example

In order for an article to be completed it must have the following rules

1. stock is > 0.
2. image url is present.
3. price exists.

```python
from collections import namedtuple
from typing import Union

from rules_engine import Otherwise, Rule, RulesEngine, then

Article = namedtuple("Article", "title price image_url stock")
article = Article(title="Iphone Case", price=1000, image_url="http://localhost/image", stock=None)


def produce_article_completed_event():
    return None


def article_controller(article: Article):
    if not article.stock:
        return False
    if not article.price:
        raise ValueError("Article price missing")
    if not article.image_url:
        raise ValueError("Article image_url missing")
    return produce_article_completed_event()
```

To be able to change to rules engine, we need to split the conditions and actions.

Rules engine is pretty simple if the condition is `True`, its corresponding action will be executed.

```python
### Conditions
def no_article_stock(article):
    return not article.stock


def no_article_price(article):
    return not article.price


def no_article_image_url(article):
    return not article.image_url

### Actions
def article_price_missing_error(article):
    raise ValueError("Article price missing")


def article_image_missing_error(article):
    raise ValueError("Article image_url missing")


### Rules Engine
def article_complete_rules(article):
    RulesEngine(
        Rule(no_article_stock, then(False)),
        Rule(no_article_price, article_price_missing_error),
        Rule(no_article_image_url, article_image_missing_error),
        Otherwise(produce_article_completed_event()),
    ).run(article)
```
