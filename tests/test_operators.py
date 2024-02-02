import pytest

from src.rules_engine import NoMatch, Rule, RulesEngine, all_, any_, not_, then, when


def raise_cannot_be_none_error(obj):
    raise ValueError("cannot be None error")


def test_when_then_operator():
    obj = None

    with pytest.raises(ValueError):
        RulesEngine(Rule(when(obj is None), raise_cannot_be_none_error)).run(obj)

    with pytest.raises(NoMatch):
        RulesEngine(Rule(when(obj is not None), raise_cannot_be_none_error)).run(obj)


@pytest.mark.parametrize(
    "condition,action,result",
    [
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
        ([when(True), when(False), when(False)], "A", "A"),
        ([when(True), when(True), when(False)], "A", "A"),
        ([when(True), when(True), when(True)], "A", "A"),
    ],
)
def test_any_operator(conditions, action, result):
    obj = None
    assert RulesEngine(Rule(any_(*conditions), then(action))).run(obj).value is result


@pytest.mark.parametrize(
    "conditions,action",
    [
        ([when(False), when(False), when(False)], "A"),
    ],
)
def test_any_operator_no_match(conditions, action):
    obj = None
    with pytest.raises(NoMatch):
        RulesEngine(Rule(any_(*conditions), then(action))).run(obj)


@pytest.mark.parametrize(
    "conditions,action,value,message",
    [
        ([when(True), when(True), when(True)], "A", "A", None),
    ],
)
def test_all_operator(conditions, action, value, message):
    obj = None

    result = RulesEngine(Rule(all_(*conditions), then(action))).run(obj)
    assert result.value == value
    assert result.message == message


@pytest.mark.parametrize(
    "conditions,action,value,message",
    [
        ([when(False), when(False), when(False)], "A", None, "No conditions matched"),
        ([when(True), when(False), when(False)], "A", None, "No conditions matched"),
        ([when(True), when(True), when(False)], "A", None, "No conditions matched"),
    ],
)
def test_all_operator_no_match(conditions, action, value, message):
    obj = None
    with pytest.raises(NoMatch):
        RulesEngine(Rule(all_(*conditions), then(action))).run(obj)
