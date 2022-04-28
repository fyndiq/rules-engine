# All

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
