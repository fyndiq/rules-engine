# When\Then

## When

Evaluates a condition.

let's check if a value is `None` and raise an exception.

```python

from rules_engine import Rule, RulesEngine, when
obj = None

def raise_cannot_be_none_error():
    raise ValueError("not a string error")

RulesEngine(Rule(when(obj is None), raise_cannot_be_none_error)).run(obj)

>>> ValueError: not a string error
```

## Then

Evaluates an action.

```python

from rules_engine import Rule, RulesEngine, when
obj = None

RulesEngine(Rule(when(obj is None), then(raise ValueError('not a string error')))).run(obj)

>>> ValueError: not a string error
```

