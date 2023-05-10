import ctypes
import sys
import traceback

from . import libui


# void uiTimer(int milliseconds, int (*f)(void *data), void *data);
_timer = libui.uiTimer
_timer.restype = None
_timer.argtypes = [
    ctypes.c_int,
    ctypes.CFUNCTYPE(
        ctypes.c_int,
        ctypes.c_void_p,
    ),
    ctypes.c_void_p,
]


class Timer(object):

    def __init__(self):
        super().__init__()
        self.callbacks = []

    def after(self, t, f):

        assert isinstance(t, (int, float))

        def _f(data):
            try:
                if f():
                    return 1
                return 0
            except KeyboardInterrupt:
                return 0
            except:  # noqa
                traceback.print_exc(file=sys.stderr)
                return 1

        cb = _timer.argtypes[1](_f)
        _timer(int(float(t) * 1000), cb, None)
        self.callbacks += [cb]

    def __del__(self):
        for cb in self.callbacks:
            del cb
