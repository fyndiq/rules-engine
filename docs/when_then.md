# When\Then

## When

Evaluates a condition.

let's check if a value is `None` and raise an exception.

```python

from rules_engine import Rule, RulesEngine, when
obj = None

def no_a_string(obj):
    return "not a string error"

RulesEngine(Rule(when(obj is None), cannot_be_none_error)).run(obj)

>>> Result(value='not a string error', message=None)>> 'not a string error'

```

## Then

Evaluates an action.

```python

from rules_engine import Rule, RulesEngine, when
obj = None

RulesEngine(Rule(when(obj is None), then('not a string error'))).run(obj)

>>> Result(value='not a string error', message=None)

```
