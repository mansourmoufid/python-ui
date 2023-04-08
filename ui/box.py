import ctypes

from . import control
from . import libui


class _Box(ctypes.Structure):
    pass


# void uiBoxAppend(uiBox *b, uiControl *child, int stretchy);
_box_append = libui.uiBoxAppend
_box_append.restype = None
_box_append.argtypes = [
    ctypes.POINTER(_Box),
    ctypes.POINTER(control._Control),
    ctypes.c_int,
]


# void uiBoxDelete(uiBox *b, int index);
_box_delete = libui.uiBoxDelete
_box_delete.restype = None
_box_delete.argtypes = [
    ctypes.POINTER(_Box),
    ctypes.c_int,
]


# int uiBoxPadded(uiBox *b);
_box_padded = libui.uiBoxPadded
_box_padded.restype = ctypes.c_int
_box_padded.argtypes = [
    ctypes.POINTER(_Box),
]


# void uiBoxSetPadded(uiBox *b, int padded);
_box_set_padded = libui.uiBoxSetPadded
_box_set_padded.restype = None
_box_set_padded.argtypes = [
    ctypes.POINTER(_Box),
    ctypes.c_int,
]


# uiBox *uiNewHorizontalBox(void);
_new_horizontal_box = libui.uiNewHorizontalBox
_new_horizontal_box.restype = ctypes.POINTER(_Box)
_new_horizontal_box.argtypes = []


# uiBox *uiNewVerticalBox(void);
_new_vertical_box = libui.uiNewVerticalBox
_new_vertical_box.restype = ctypes.POINTER(_Box)
_new_vertical_box.argtypes = []


class Box(control.Control):

    def __init__(self, padded=True, **kwargs):
        super(Box, self).__init__(**kwargs)
        self.ctrl = self.box
        self.padded(padded)

    def append(self, x, stretchy=False):
        assert isinstance(x, control.Control)
        assert isinstance(stretchy, bool)
        _box_append(self.box, x.control(), 1 if stretchy else 0)

    def delete(self, i):
        assert isinstance(i, int)
        _box_delete(self.box, i)

    def padded(self, x=None):
        assert x is None or isinstance(x, bool)
        if x is None:
            return not _box_padded(self.box) == 0
        else:
            _box_set_padded(self.box, 1 if x else 0)

    def __add__(self, x):
        self.append(x)
        return self


class HorizontalBox(Box):

    def __new__(cls, *args, **kwargs):
        x = super(HorizontalBox, cls).__new__(cls)
        x.box = _new_horizontal_box()
        return x


class VerticalBox(Box):

    def __new__(cls, *args, **kwargs):
        x = super(VerticalBox, cls).__new__(cls)
        x.box = _new_vertical_box()
        return x
