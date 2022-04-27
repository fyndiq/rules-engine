# Any

Evaluates multiple conditions and if any of conditions is `True` the action is excuted

- Example:
    - We need to check if an object `obj` is a `str` or `list`


```python

from rules_engine import Rule, RulesEngine, any_

def is_a_str(obj):
    return isinstance(obj, str)

def is_a_list(obj):
    return isinstance(obj, list)

obj="Hello"

RulesEngine(Rule(any_(is_a_str, is_a_list), then(True))).run(obj)

>>> True
```
