import pytest

from src.rules_engine import Result


@pytest.mark.parametrize(
    "value, message, expected_result",
    [
        (True, "Success", True),
        ("aaa", "Success", True),
        (2, "Success", True),
        (False, None, False),
        (None, None, False),
        (False, "Failure", False),
    ],
)
def test_result(value, message, expected_result):
    result = Result(value, message)
    assert bool(result) is expected_result
