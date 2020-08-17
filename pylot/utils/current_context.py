from typing import Optional

from . import message_with_context
from .design_by_contract import ensure_postcondition
from .threads import threadLocal


class CurrentContext:
    @classmethod
    def _key(cls):
        return cls.__qualname__

    @classmethod
    def current(cls) -> 'CurrentContext':
        ret = cls.try_get_current()
        ensure_postcondition(ret, lambda: message_with_context("There is current context", context_type=cls._key()))
        return ret

    @classmethod
    def try_get_current(cls) -> Optional['CurrentContext']:
        return getattr(threadLocal, cls._key()) if hasattr(threadLocal, cls._key()) else None

    _oldCurrent = None

    def __enter__(self):
        self._oldCurrent = getattr(threadLocal, self._key(), None)
        threadLocal.__setattr__(self._key(), self)
        return self

    def __exit__(self, *args): #type, value, traceback
        threadLocal.__setattr__(self._key(), self._oldCurrent)
