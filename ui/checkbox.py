import ctypes

from . import control
from . import decode, encode
from . import libui


class _Checkbox(ctypes.Structure):
    pass


# char *uiCheckboxText(uiCheckbox *c);
_checkbox_text = libui.uiCheckboxText
_checkbox_text.restype = ctypes.c_char_p
_checkbox_text.argtypes = [
    ctypes.POINTER(_Checkbox),
]


# void uiCheckboxSetText(uiCheckbox *c, const char *text);
_checkbox_set_text = libui.uiCheckboxSetText
_checkbox_set_text.restype = None
_checkbox_set_text.argtypes = [
    ctypes.POINTER(_Checkbox),
    ctypes.c_char_p,
]


# uiCheckbox *uiNewCheckbox(const char *text);
_new_checkbox = libui.uiNewCheckbox
_new_checkbox.restype = ctypes.c_void_p
_new_checkbox.argtypes = [
    ctypes.c_char_p,
]


# void uiCheckboxOnToggled(
#   uiCheckbox *c,
#   void (*f)(uiCheckbox *c, void *data),
#   void *data
# );
_checkbox_on_toggled = libui.uiCheckboxOnToggled
_checkbox_on_toggled.restype = None
_checkbox_on_toggled.argtypes = [
    ctypes.POINTER(_Checkbox),
    ctypes.CFUNCTYPE(
        None,
        ctypes.POINTER(_Checkbox),
        ctypes.c_void_p,
    ),
    ctypes.c_void_p,
]


# int uiCheckboxChecked(uiCheckbox *c);
_checkbox_checked = libui.uiCheckboxChecked
_checkbox_checked.restype = ctypes.c_int
_checkbox_checked.argtypes = [
    ctypes.POINTER(_Checkbox),
]


# void uiCheckboxSetChecked(uiCheckbox *c, int checked);
_checkbox_set_checked = libui.uiCheckboxSetChecked
_checkbox_set_checked.restype = None
_checkbox_set_checked.argtypes = [
    ctypes.POINTER(_Checkbox),
    ctypes.c_int,
]


class Checkbox(control.Control):

    def __init__(self, text, checked=False, on_toggled=None, **kwargs):

        super(Checkbox, self).__init__(**kwargs)

        assert isinstance(text, str)
        self.checkbox = ctypes.cast(
            _new_checkbox(encode(text)),
            ctypes.POINTER(_Checkbox),
        )
        self.ctrl = self.checkbox
        self.callbacks = []

        self.checked(checked)
        self.set_on_toggled(on_toggled)

    def text(self, x=None):
        assert x is None or isinstance(x, str)
        if x is None:
            return decode(_checkbox_text(self.checkbox))
        else:
            _checkbox_set_text(self.checkbox, encode(x))

    def on_toggled(self):
        pass

    def set_on_toggled(self, f=None):

        if f is None:
            return
        self.on_toggled = f

        def _on_toggled(checkbox, data):
            return self.on_toggled()

        cb = _checkbox_on_toggled.argtypes[1](_on_toggled)
        _checkbox_on_toggled(self.checkbox, cb, None)
        self.callbacks += [cb]

    def checked(self, x=None):
        assert x is None or isinstance(x, bool)
        if x is None:
            return not _checkbox_checked(self.checkbox) == 0
        else:
            _checkbox_set_checked(self.checkbox, 1 if x else 0)
