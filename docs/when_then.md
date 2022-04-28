# When\Then

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

