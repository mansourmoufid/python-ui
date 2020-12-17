import ctypes

from . import control
from . import decode, encode
from . import libui


class _Label(ctypes.Structure):
    pass


# char *uiLabelText(uiLabel *l);
_label_text = libui.uiLabelText
_label_text.restype = ctypes.c_char_p
_label_text.argtypes = [
    ctypes.POINTER(_Label),
]


# void uiLabelSetText(uiLabel *l, const char *text);
_label_set_text = libui.uiLabelSetText
_label_set_text.restype = None
_label_set_text.argtypes = [
    ctypes.POINTER(_Label),
    ctypes.c_char_p,
]


# uiLabel *uiNewLabel(const char *text);
_new_label = libui.uiNewLabel
_new_label.restype = ctypes.c_void_p
_new_label.argtypes = [
    ctypes.c_char_p,
]


class Label(control.Control):

    def __init__(self, text=None):

        super(Label, self).__init__()

        assert text is None or isinstance(text, str)
        self.label = ctypes.cast(
            _new_label(encode(text or '')),
            ctypes.POINTER(_Label)
        )
        self.ctrl = self.control(self.label)

    def text(self, x=None):
        assert x is None or isinstance(x, str)
        if x is None:
            return decode(_label_text(self.label))
        else:
            _label_set_text(self.label, encode(x))
