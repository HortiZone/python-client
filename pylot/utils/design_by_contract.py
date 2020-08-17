from typing import Any, Union, Callable

from .utils import message_with_context, T


def postcondition_violated(condition_text: str, **kwargs):
    raise PostConditionViolated(message_with_context("Postcondition violated: " + condition_text, **kwargs))


def precondition_violated(condition_text: str, **kwargs):
    raise PreConditionViolated(message_with_context("Precondition violated: " + condition_text, **kwargs))


def ensure_precondition(condition: Any, rule_text: Union[str, Callable[[], str]], **kwargs):
    if not condition:
        if callable(rule_text):
            raise precondition_violated(rule_text(), **kwargs)
        else:
            raise precondition_violated(rule_text, **kwargs)


def ensure_postcondition(condition: Any, rule_text: Union[str, Callable[[], str]], **kwargs):
    if not condition:
        if callable(rule_text):
            raise postcondition_violated(rule_text(), **kwargs)
        else:
            raise postcondition_violated(rule_text, **kwargs)


def ensure_non_empty(value: T, value_name: str, **kwargs) -> T:
    ensure_precondition(value, value_name + " must be non empty", **kwargs)
    return value


def ensure_constraint(rule_condition, rule_text, **kwargs):
    if not rule_condition:
        raise ConstraintViolated("Constraint violated: " + message_with_context(rule_text, **kwargs))


class PostConditionViolated(Exception):
    pass


class PreConditionViolated(Exception):
    pass

class ConstraintViolated(Exception):
    pass
