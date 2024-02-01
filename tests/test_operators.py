import pytest

from src.rules_engine import Rule, RulesEngine, all_, any_, not_, then, when


def raise_cannot_be_none_error(obj, message):
    raise ValueError("cannot be None error")


def test_when_then_operator():
    obj = None

    with pytest.raises(ValueError):
        RulesEngine(Rule(when(obj is None), raise_cannot_be_none_error)).run(obj)

    assert RulesEngine(Rule(when(obj is not None), then(True))).run(obj) is None


@pytest.mark.parametrize(
    "condition,action,result",
    [
        (True, True, None),
        (False, "A", "A"),
        (False, "B", "B"),
    ],
)
def test_not_operator(condition, action, result):
    obj = None

    assert RulesEngine(Rule(not_(when(condition)), then(action))).run(obj) is result


@pytest.mark.parametrize(
    "conditions,action,result",
    [
        ([when(False), when(False), when(False)], "A", None),
        ([when(True), when(False), when(False)], "A", "A"),
        ([when(True), when(True), when(False)], "A", "A"),
        ([when(True), when(True), when(True)], "A", "A"),
    ],
)
def test_any_operator(conditions, action, result):
    obj = None

    assert RulesEngine(Rule(any_(*conditions), then(action))).run(obj) is result


@pytest.mark.parametrize(
    "conditions,action,result",
    [
        ([when(False), when(False), when(False)], "A", None),
        ([when(True), when(False), when(False)], "A", None),
        ([when(True), when(True), when(False)], "A", None),
        ([when(True), when(True), when(True)], "A", "A"),
    ],
)
def test_all_operator(conditions, action, result):
    obj = None

    assert RulesEngine(Rule(all_(*conditions), then(action))).run(obj) is result
