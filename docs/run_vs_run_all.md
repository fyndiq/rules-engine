# Run/RunAll

## Run

Runs rules sequentially and exists executes the action for the first passing condition.

```python

from rules_engine import Rule, RulesEngine, then
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

## RunAll

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
