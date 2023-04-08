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
        super(Timer, self).__init__()
        self.callbacks = []

    def after(self, t, f):

        assert isinstance(t, (int, float))

        def _f(data):
            try:
                return f()
            except:  # noqa
                traceback.print_exc(file=sys.stderr)
                return 0

        cb = _timer.argtypes[1](_f)
        _timer(int(float(t) * 1000), cb, None)
        self.callbacks += [cb]

    def __del__(self):
        for cb in self.callbacks:
            del cb
