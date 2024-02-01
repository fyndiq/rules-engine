import pytest

from src.rules_engine import Rule, RulesEngine, all_, any_, not_, then, when


def raise_cannot_be_none_error(obj):
    raise ValueError("cannot be None error")


def test_when_then_operator():
    obj = None

    with pytest.raises(ValueError):
        RulesEngine(Rule(when(obj is None), raise_cannot_be_none_error)).run(obj)

    result = RulesEngine(Rule(when(obj is not None), then(True), "obj is None")).run(obj)
    assert result.value is None
    assert result.message == "No conditions matched"


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

    assert RulesEngine(Rule(not_(when(condition)), then(action))).run(obj).value is result


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

    assert RulesEngine(Rule(any_(*conditions), then(action))).run(obj).value is result


@pytest.mark.parametrize(
    "conditions,action,value,message",
    [
        ([when(False), when(False), when(False)], "A", None, "No conditions matched"),
        ([when(True), when(False), when(False)], "A", None, "No conditions matched"),
        ([when(True), when(True), when(False)], "A", None, "No conditions matched"),
        ([when(True), when(True), when(True)], "A", "A", None),
    ],
)
def test_all_operator(conditions, action, value, message):
    obj = None

    result = RulesEngine(Rule(all_(*conditions), then(action))).run(obj)
    assert result.value == value
    assert result.message == message
