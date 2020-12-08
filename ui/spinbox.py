import ctypes

from . import control
from . import libui


class _Spinbox(ctypes.Structure):
    pass


# int uiSpinboxValue(uiSpinbox *s);
_spinbox_value = libui.uiSpinboxValue
_spinbox_value.restype = ctypes.c_int
_spinbox_value.argtypes = [
    ctypes.POINTER(_Spinbox),
]


# void uiSpinboxSetValue(uiSpinbox *s, int value);
_spinbox_set_value = libui.uiSpinboxSetValue
_spinbox_set_value.restype = None
_spinbox_set_value.argtypes = [
    ctypes.POINTER(_Spinbox),
    ctypes.c_int,
]


# void uiSpinboxOnChanged(
#   uiSpinbox *s,
#   void (*f)(uiSpinbox *s, void *data),
#   void *data
# );
_spinbox_on_changed = libui.uiSpinboxOnChanged
_spinbox_on_changed.restype = None
_spinbox_on_changed.argtypes = [
    ctypes.POINTER(_Spinbox),
    ctypes.CFUNCTYPE(
        None,
        ctypes.POINTER(_Spinbox),
        ctypes.c_void_p,
    ),
    ctypes.c_void_p,
]


# uiSpinbox *uiNewSpinbox(int min, int max);
_new_spinbox = libui.uiNewSpinbox
_new_spinbox.restype = ctypes.POINTER(_Spinbox)
_new_spinbox.argtypes = [
    ctypes.c_int,
    ctypes.c_int,
]


class Spinbox(control.Control):

    def __init__(self, min=0, max=100, value=0):

        super(Spinbox, self).__init__()

        assert isinstance(min, int)
        assert isinstance(max, int)
        self.min, self.max = min, max

        self.spinbox = _new_spinbox(self.min, self.max)
        self.ctrl = self.control(self.spinbox)

        def onchanged(spinbox, data):
            return self.on_changed()

        cb = _spinbox_on_changed.argtypes[1](onchanged)
        _spinbox_on_changed(self.spinbox, cb, None)
        self.callbacks = [cb]

        self.value(value)

    def on_changed(self):
        pass

    def value(self, x=None):
        if x is None:
            return int(_spinbox_value(self.spinbox))
        else:
            assert isinstance(x, int)
            _spinbox_set_value(self.spinbox, x)
