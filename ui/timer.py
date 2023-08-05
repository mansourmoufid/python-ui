import ctypes
import sys
import traceback
import typing

from . import libui


_timer_callback_t = ctypes.CFUNCTYPE(
    ctypes.c_int,
    ctypes.c_void_p,
)

# void uiTimer(int milliseconds, int (*f)(void *data), void *data);
_timer = libui.uiTimer
_timer.restype = None
_timer.argtypes = [
    ctypes.c_int,
    _timer_callback_t,
    ctypes.c_void_p,
]


class Timer(object):

    def __init__(self) -> None:
        super().__init__()
        self.callbacks: typing.List[typing.Callable] = []

    def after(
        self,
        t: typing.Union[int, float],
        f: typing.Callable[[], typing.Union[bool, int]]
    ) -> None:

        def _f(data: ctypes.c_void_p) -> int:
            try:
                if f():
                    return 1
                return 0
            except KeyboardInterrupt:
                return 0
            except:  # noqa
                traceback.print_exc(file=sys.stderr)
                return 1

        cb = _timer_callback_t(_f)
        _timer(int(float(t) * 1000), cb, None)
        self.callbacks += [cb]

    def __del__(self):
        for cb in tuple(self.callbacks):
            self.callbacks.remove(cb)
            del cb
