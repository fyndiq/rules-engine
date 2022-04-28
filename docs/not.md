# Not

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
