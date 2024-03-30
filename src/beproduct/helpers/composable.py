import functools as ft
import inspect


def _chain(*callables):
    return ft.partial(ft.reduce, lambda acc, func: func(acc), callables)


class Composable(object):

    __slots__ = ("_callable",)

    def __init__(self, func):
        assert len(inspect.signature(func).parameters) == 1, ""
        self._callable = func

    def __call__(self, *args, **kwargs):
        return self._callable(*args, **kwargs)

    def __ror__(self, lhe):
        if callable(lhe):
            return composable(_chain(self._callable, lhe))
        return self(lhe)

    def __or__(self, rhe):
        assert callable(rhe)
        return composable(_chain(rhe, self._callable))


def composable(func, *args, **kwargs):
    """Function decorator to make a function composable"""
    return Composable(ft.partial(func, *args, **kwargs))
