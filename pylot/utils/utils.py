from itertools import chain
from typing import TypeVar, Callable, Iterable, List

KT = TypeVar('KT')
VT = TypeVar('VT')
T = TypeVar('T')
T1 = TypeVar('T1')
T2 = TypeVar('T2')


def join_list(iterable, separator=","):
    return separator.join(map(str, iterable))


def message_with_context(msg: str, **kwargs) -> str:
    return (msg + ". " if msg[-1:] != '.' else msg[:-1] + ' ') + context_to_str(**kwargs)


def context_to_str(**kwargs):
    return join_list((str(key) + ":" + str(value) for key, value in kwargs.items()), ", ")

def flatmap(fn: Callable[[T1], Iterable[T2]], items: Iterable[T1]) -> List[T2]:
    return list(chain.from_iterable(map(fn, items)))
