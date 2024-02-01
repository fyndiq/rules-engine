from typing import Any, Callable, TypeVar, Optional

T = TypeVar('T')


class Rule:
    def __init__(
        self,
        condition: Callable[..., bool],
        action: Callable[..., Any],
        message: Optional[str] = None,
    ) -> None:
        self.condition = condition
        self.action = action
        self.message = message


class Otherwise(Rule):
    def __init__(self, action, message=None) -> None:
        super().__init__(when(True), action, message)


class NoAction(Rule):
    def __init__(self, condition, message=None):
        super().__init__(condition, then(None), message)


class RulesEngine:
    def __init__(self, *rules: Rule) -> None:
        self.rules = rules

    def run(self, *args: Any, **kwargs: Any) -> Any:
        for rule in self.rules:
            if rule.condition(*args, **kwargs, message=rule.message):
                return rule.action(*args, **kwargs, message=rule.message)

    def run_all(self, *args: Any, **kwargs: Any) -> list:
        return [
            rule.action(*args, **kwargs, message=rule.message)
            for rule in self.rules
            if rule.condition(*args, **kwargs, message=rule.message)
        ]


def when(state: bool) -> Callable[..., bool]:
    return lambda *args, **kwargs: state


def then(value: T) -> Callable[..., T]:
    return lambda *args, **kwargs: value


def all_(*conditions: Callable[..., bool]) -> Callable[..., bool]:
    return lambda *args, **kwargs: all(condition(*args, **kwargs) for condition in conditions)


def any_(*conditions: Callable[..., bool]) -> Callable[..., bool]:
    return lambda *args, **kwargs: any(condition(*args, **kwargs) for condition in conditions)


def not_(condition: Callable[..., bool]) -> Callable[..., bool]:
    return lambda *args, **kwargs: not condition(*args, **kwargs)
